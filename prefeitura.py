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
from dotenv import load_dotenv

def process_prefeitura(im:str, mes:str, ano:str, numero_nota:str):

    # Carrega as variáveis do .env
    load_dotenv()

    user = os.getenv("ACESSO_PREFEITURA")
    password = os.getenv("PASSWORD_PREFEITURA")
    
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

    url = 'https://sispmjp.joaopessoa.pb.gov.br:8080/sispmjp/login.jsf'

    try:

        driver.get(url)

        write('//*[@id="j_username"]', user, driver)

        write('//*[@id="j_password"]', password, driver)

        click('//*[@id="commandButton_entrar"]', driver)

        click('//*[@id="formAtualizarContato:commandButton_confirmar_mais_tarde"]/span[2]', driver)

        time.sleep(0.2)

        driver.get('https://sispmjp.joaopessoa.pb.gov.br:8080/sispmjp/paginas/ds/DS_GerenciarContribuinte.jsf')

        write('//*[@id="form:contribuintesVinculados:j_idt64:filter"]', im, driver)

        click('//*[@id="form:contribuintesVinculados:0:commandButton_representarContribuinte"]/span[1]', driver)

        time.sleep(0.2)

        driver.get('https://sispmjp.joaopessoa.pb.gov.br:8080/sispmjp/paginas/ds/DS_EntregarDeclaracaoTomador.jsf')

        write('//*[@id="formEntregarDeclaracaoTomador:mes"]', mes, driver)

        write('//*[@id="formEntregarDeclaracaoTomador:ano"]', ano, driver)

        click('//*[@id="formEntregarDeclaracaoTomador:confirmarButton"]/span[2]', driver)

        click('//*[@id="form_lista_notas_declaracoes:commandButton_incluirDocumento"]/span', driver)

        write('//*[@id="form_emitir_nfse_ne:input_num_nota"]', numero_nota, driver)

        click('//*[@id="form_emitir_nfse_ne:commandButton_continuar"]/span[2]', driver)

        time.sleep(5)

    except Exception as e:

        print(f"ERRO: {e}")

    
process_prefeitura('1484176', '01', '2025', '123456')