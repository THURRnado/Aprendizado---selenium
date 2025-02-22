'''sefaz pb
sefaz virrtal

01/22/2024 - 30/11/2024

161476090 - IE Gm comercio
163805814 - IE DA TROPICAL DISTRIBUIDORA
161339387 - IE DA ABC DISTRIBUIDOR

Servicos para empresa - Tributos - Pagamentos - Consultar extratos de Pagamento por contribuinte

preencher os dados'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from metodos_selenium import write, click, iframe, iframe_end, scroll_to_element
from dotenv import load_dotenv
from manipulacao_arquivos import extract_and_save_tables

def download_extrato_de_pag(ie:str, data_inicio:str, data_final:str):

    load_dotenv()

    user_name = os.getenv("USER_NAME")
    user_password = os.getenv("USER_PASSWORD")

    # Define o diretório onde os arquivos serão baixados
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

        driver.get('https://www4.sefaz.pb.gov.br/atf/arr/ARRf_ConsultarExtrPgtoCont.do?idSERVirtual=S&amp;h=https://www.sefaz.pb.gov.br/ser/servirtual/credenciamento/info')

        write('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input[3]', data_inicio, driver)

        write('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input[4]', data_final, driver)

        iframe('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[5]/td/table/tbody/tr[2]/td/iframe', driver)

        write('//*[@id="Layer1"]/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input', ie, driver)

        click('//*[@id="Layer1"]/table/tbody/tr/td/form/table/tbody/tr[1]/td[3]/input', driver)

        iframe_end(driver)

        click('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[6]/td/input', driver)
        
        time.sleep(1)

        # Caminho para a pasta
        directory = os.path.join(os.getcwd(), "uploads", "pdf")

        # Listar todos os arquivos na pasta
        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        # Verificar se há arquivos na pasta
        file_path = max(files, key=os.path.getmtime)

        # Diretório para salvar os arquivos
        output_dir = os.path.join(os.getcwd(), "uploads", "pdf") 
        extract_and_save_tables(file_path, output_dir)

    except Exception as e:

        print(f'Houve um erro - {e}')

    finally:

        driver.quit()

lista_de_empresas = ['161476090', '163805814', '161339387']
data_inicio = '01/10/2024'
data_final = '30/11/2024'

for ie in lista_de_empresas:
    download_extrato_de_pag(ie, data_inicio, data_final)