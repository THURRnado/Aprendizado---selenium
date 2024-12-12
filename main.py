import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from lxml import html

from bs4 import BeautifulSoup

teams_address_A = {'palmeiras' : 'palmeiras/1963', 'internacional' : 'internacional/1966', 'flamengo' : 'flamengo/5981', 'fluminense' : 'fluminense/1961','corinthians' : 'corinthians/1957', 'athletico paranaense' : 'athletico/1967', 'atletico mineiro' : 'atletico-mineiro/1977','fortaleza' : 'fortaleza/2020', 'botafogo' : 'botafogo/1958', 'sao paulo' : 'sao-paulo/1981', 'bragantino' : 'red-bull-bragantino/1999','cuiaba' : 'cuiaba/49202', 'atletico goianiense' : 'atletico-goianiense/7314', 'juventude' : 'juventude/1980','criciuma' : 'criciuma/1984','vitoria':'vitoria/1962','gremio' : 'gremio/5926','bahia' : 'bahia/1955','cruzeiro' : 'cruzeiro/1954','vasco' : 'vasco-da-gama/1974'}

def team_search(time:str):

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    base_url = 'https://www.sofascore.com/pt/time/futebol/'

    url = base_url + teams_address_A[time]

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lmxl')

    conteudo = str(soup)

    estrutura = html.fromstring(conteudo)