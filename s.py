import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from vars import URL

# Создание объекта ChromeOptions для дополнительных настроек браузера
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('--no-sandbox')
options_chrome.add_argument('--headless')
options_chrome.add_argument('--disable-dev-shm-usage')

with webdriver.Chrome(options=options_chrome) as browser:
    # Открытие сайта в браузере
    browser.get(URL)

    text = browser.find_element(
        By.CSS_SELECTOR,
        "#app > div.main-view > div.main-container > div > div.hero-params > div > div.title")

    print(text.text)

    browser.save_screenshot("page.png")

    # soup = BeautifulSoup(browser.page_source,  'lxml')
    # headings = soup.find('div',  {'class': 'elementor-heading-title'})
    # time.sleep(10)
    # for heading in headings:
    #     print(heading.getText())
