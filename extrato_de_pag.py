'''sefaz pb
sefaz virrtal

01/22/2024 - 30/11/2024

16.147.609-0

Servicos para empresa - Tributos - Pagamentos - Consultar extratos de Pagamento por contribuinte

preencher os dados'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from metodos_selenium import write, click, iframe, iframe_end
from dotenv import load_dotenv

def download_extrato_de_pag():

    load_dotenv()

    user = os.getenv("SEFAZ_USER")
    password = os.getenv("SEFAZ_PASSWORD")

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

        iframe('//*[@id="atf-login"]/iframe', driver)

        #Preenchendo o campo de login
        write('//*[@id="form-cblogin-username"]/div/input', user, driver)

        #Preenchendo o campo de senha
        write('//*[@id="form-cblogin-password"]/div[1]/input', password, driver)

        click('//*[@id="form-cblogin-password"]/div[2]/input[2]', driver)

        iframe_end(driver)

        driver.get('https://www4.sefaz.pb.gov.br/atf/arr/ARRf_ConsultarExtrPgtoCont.do?idSERVirtual=S&amp;h=https://www.sefaz.pb.gov.br/ser/servirtual/credenciamento/info')

        write('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input[3]', '01/11/2024', driver)

        write('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input[4]', '30/11/2024', driver)

        iframe('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[5]/td/table/tbody/tr[2]/td/iframe', driver)

        write('//*[@id="Layer1"]/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input', '161476090', driver)

        click('//*[@id="Layer1"]/table/tbody/tr/td/form/table/tbody/tr[1]/td[3]/input', driver)

        iframe_end(driver)

        click('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[6]/td/input', driver)
        
        time.sleep(0.5)

    finally:

        driver.quit()

download_extrato_de_pag()
