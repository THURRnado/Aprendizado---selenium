from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil

def test_click():

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Abrir o Google
        driver.get("https://www.youtube.com/")

        # Localizar o campo de input usando XPath
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="center"]/yt-searchbox/div[1]/form/input'))
        )

        # Preencher o campo com "videos legais" e pressionar Enter
        search_box.send_keys("videos legais" + Keys.RETURN)

        # Esperar alguns segundos para carregar os resultados
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'video-title')))

        # Localizar o elemento usando XPath
        thumbnail = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="thumbnail"]/yt-image/img'))
        )

        # Clicar no elemento
        thumbnail.click()

        time.sleep(10)

    finally:
        # Fechar o navegador
        driver.quit()


# Para baixar o historico de um usuario do sigaa para o diretório passado
def test_download():

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
        "safebrowsing.enabled": True                # Ativa a segurança para downloads
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = 'https://sigaa.ufpb.br/sigaa/public/home.jsf;jsessionid=25FEE3707C0A09E60A7A6D701EE9BED5'
    
    try:

        # Abrir a url
        driver.get(url)

        # Aguarde até que o elemento esteja clicável
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-acessibilidade"]/li[5]/a'))
        )

        # Clique no elemento
        link.click()

        # Aguarde até que o campo de texto esteja presente e visível
        campo_login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form:login"]'))
        )

        # Limpe o campo (opcional) e insira o texto
        campo_login.clear()  # Limpa o campo caso tenha texto pré-existente
        campo_login.send_keys("")

        campo_senha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form:senha"]'))
        )

        campo_senha.clear()
        campo_senha.send_keys("")

        # Aguarde até que o elemento esteja clicável
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form:entrar"]'))
        )

        # Clique no elemento
        button.click()

        # Aguarde até que o elemento esteja clicável
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main-menu"]/li[1]/a'))
        )

        # Clique no elemento
        button.click()

        # Aguarde até que o elemento esteja clicável
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main-menu"]/li[1]/ul/li[3]/a'))
        )

        # Clique no elemento
        button.click()

        time.sleep(1)

    finally:

        driver.quit()


# Função para mover um pdf de uma pasta para a outra
def move_latest_pdf_from_downloads(download_dir, upload_dir):
    """
    Move o último arquivo PDF do diretório Downloads para uploads/pdf

    :param download_dir: Diretório onde os PDFs são baixados (padrão: Downloads)
    :param upload_dir: Diretório onde o arquivo será movido
    """
    # Certifique-se de criar o diretório, se necessário
    os.makedirs(upload_dir, exist_ok=True)

    # Listar arquivos PDF no diretório Downloads
    files = [f for f in os.listdir(download_dir) if f.endswith('.pdf')]

    if not files:
        print("Nenhum arquivo PDF encontrado.")
        return

    # Encontrar o último arquivo baseado na data de modificação
    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(download_dir, x)))

    # Caminho completo do destino
    destination_path = os.path.join(upload_dir, latest_file)

    print(f"Último arquivo encontrado: {latest_file}")
    
    # Move o arquivo
    shutil.move(os.path.join(download_dir, latest_file), destination_path)

    print(f"Arquivo {latest_file} movido para {destination_path}")


test_download()

# Diretório padrão do Windows para downloads
#download_dir = r"D:\Downloads"

# Diretório de destino para uploads/pdf
#upload_dir = os.path.join(os.getcwd(), "uploads", "pdf")

#move_latest_pdf_from_downloads(download_dir, upload_dir)