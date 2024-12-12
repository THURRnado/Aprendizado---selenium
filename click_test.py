from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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


test_click()