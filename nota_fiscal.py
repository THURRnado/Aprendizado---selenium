from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from metodos_selenium import write, click, iframe, iframe_end
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def download_nota_fiscal():
    
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

        iframe('//*[@id="atf-login"]/iframe', driver)

        #Preenchendo o campo de login
        write('//*[@id="form-cblogin-username"]/div/input', 'hel00012', driver)

        #Preenchendo o campo de senha
        write('//*[@id="form-cblogin-password"]/div[1]/input', 'Asdf3340', driver)

        click('//*[@id="form-cblogin-password"]/div[2]/input[2]', driver)

        iframe_end(driver)

        driver.get('https://www.sefaz.pb.gov.br/servirtual/documentos-fiscais/nf-e/consulta-emitentes-destinatarios')

        driver.get('https://www4.sefaz.pb.gov.br/atf/fis/FISf_ConsultarNFeXml2.do?idSERVirtual=S&amp;h=https://www.sefaz.pb.gov.br/ser/servirtual/credenciamento/info')

        write('/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/input[1]', '01/11/2024', driver)

        write('/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/input[2]', '30/11/2024', driver)

        iframe('/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[7]/td/table/tbody/tr[2]/td/iframe', driver)

        write('//*[@id="Layer1"]/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input', '161476090', driver)

        click('//*[@id="Layer1"]/table/tbody/tr/td/form/table/tbody/tr[1]/td[3]/input', driver)

        time.sleep(0.5)

        iframe_end(driver)

        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[12]/td/select'))
        )

        select = Select(select_element)

        select.select_by_index(1)  

        click('//*[@id="btnConsulta"]', driver)

        time.sleep(5)

        driver.get('https://www.sefaz.pb.gov.br/servirtual/caixa-de-mensagens')

        time.sleep(30)

    finally:

        driver.quit()


download_nota_fiscal()