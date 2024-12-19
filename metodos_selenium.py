from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def write(xpath:str, text:str, driver):
    campo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    campo.clear()
    campo.send_keys(text)

    return

def click(xpath:str, driver):
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    button.click()

    return 

def iframe(xpath:str, driver):
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    driver.switch_to.frame(iframe)

    return 

def iframe_end(driver):
     driver.switch_to.default_content()

     return