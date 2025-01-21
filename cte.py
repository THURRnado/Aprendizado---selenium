from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from metodos_selenium import write, click, iframe, iframe_end, get_text, scroll_to_element
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

def process(driver, option:int, dt_start:str, dt_end:str, ie:str):

    driver.get('https://www.sefaz.pb.gov.br/servirtual/documentos-fiscais/ct-e/consulta-remetente-destinatario-tomador-prestador')

    driver.get('https://www4.sefaz.pb.gov.br/atf/fis/FISf_ConsultarCTeGenerica.do?idSERVirtual=S&amp;h=https://www.sefaz.pb.gov.br/ser/servirtual/credenciamento/info')

    write('/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/input[1]', dt_start, driver)

    write('/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/input[2]', dt_end, driver)

    iframe('/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[16]/td/table/tbody/tr[2]/td/iframe', driver)

    if option == 1:
        write('//*[@id="Layer1"]/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input', ie, driver)
    else:
        write('//*[@id="Layer1"]/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input', '', driver)

    click('//*[@id="Layer1"]/table/tbody/tr/td/form/table/tbody/tr[1]/td[3]/input', driver)

    time.sleep(0.5)

    iframe_end(driver)

    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[31]/td[2]/select'))
    )

    select = Select(select_element)

    select.select_by_index(option)  

    click('//*[@id="btnConsulta"]', driver)

    time.sleep(3)

    driver.get('https://www.sefaz.pb.gov.br/servirtual/caixa-de-mensagens')

    time.sleep(1)

    driver.get('https://www4.sefaz.pb.gov.br/atf/seg/SEGf_MinhasMensagens.do?idSERVirtual=S&amp;h=https://www.sefaz.pb.gov.br/ser/servirtual/credenciamento/info')

    date = get_text('/html/body/form/div/table/tbody/tr[3]/td[6]/a', driver)

    print(f'Esse é o time da ultima mensagem: {date}')

    count = 0

    while True:

        if count > 2:
            break

        time.sleep(30)

        # Recarrega a página
        driver.refresh()

        try:
            # Tenta clicar no elemento
            click('/html/body/form/div/table/tbody/tr[3]/td[3]/a', driver)

            # Se o clique for bem-sucedido, sai do loop
            print("Clique realizado com sucesso!")
            break
        except TimeoutException:
            count = count + 1
            # Caso o clique falhe, continua no loop
            print("Elemento não encontrado. Recarregando a página...")

    try:

        click('/html/body/form/div/table/tbody/tr[5]/td[3]/a', driver)

        click('/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[8]/td/a', driver)

        time.sleep(5)

    except Exception as e:

        print("Elementos não encontrados!")


def download_nota_fiscal():

    load_dotenv()

    user_name = os.getenv("USER_NAME")
    user_password = os.getenv("USER_PASSWORD")
    
    download_dir = os.path.join(os.getcwd(), "uploads", "pdf")

    # Cria o diretório, se não existir
    os.makedirs(download_dir, exist_ok=True)

    # Configura as opções do Chrome
    chrome_options = Options()
    chrome_prefs = {
        "download.default_directory": download_dir,  # Define o diretório de download
        "download.prompt_for_download": False,       # Não pergunta antes de baixar
        "download.directory_upgrade": True,         # Atualiza automaticamente o diretório de download
        "safebrowsing.enabled": True ,               # Ativa a segurança para downloads
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    '''# Parte que desativa a janela do chrome
    chrome_options.add_argument("--headless")  # Roda o Chrome sem interface gráfica
    chrome_options.add_argument("--disable-gpu")  # Necessário para algumas versões do Chrome
    chrome_options.add_argument("--window-size=1920,1080")  # Tamanho da janela no modo headless
    chrome_options.add_argument("--no-sandbox")  # Recomendado para servidores
    chrome_options.add_argument("--disable-dev-shm-usage")  # Resolve problemas de memória compartilhada

    driver = webdriver.Chrome(options=chrome_options)'''

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = 'https://www.sefaz.pb.gov.br/servirtual'
    
    try:

        # Abrir a url
        driver.get(url)

        # Scrollar até o elemento especificado
        scroll_to_element('//*[@id="full-content"]', driver)

        iframe('//*[@id="atf-login"]/iframe', driver)

        #Preenchendo o campo de login
        write('//*[@id="form-cblogin-username"]/div/input', user_name, driver)

        #Preenchendo o campo de senha
        write('//*[@id="form-cblogin-password"]/div[1]/input', user_password, driver)

        click('//*[@id="form-cblogin-password"]/div[2]/input[2]', driver)

        iframe_end(driver)

        # Consultar TXT
        process(driver, 1, '01/09/2024', '30/11/2024', '161476090')
        # Consultar XML
        process(driver, 2, '01/09/2024', '30/11/2024', '161476090')

    finally:

        driver.quit()


download_nota_fiscal()


'''

linha 1: 

anexo: /html/body/form/div/table/tbody/tr[3]/td[3]/a

date: /html/body/form/div/table/tbody/tr[3]/td[6]/a


linha 2:

anexo: /html/body/form/div/table/tbody/tr[5]/td[3]/a

date: /html/body/form/div/table/tbody/tr[5]/td[6]/a

linha 3:

anexo: /html/body/form/div/table/tbody/tr[7]/td[3]/a

date: /html/body/form/div/table/tbody/tr[7]/td[6]/a

'''