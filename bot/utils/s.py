import time
from fileinput import close
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from bot.utils.selen_utils import close_modal, login_btn_press, phone_number_press
from bot.vars import URL

# Создание объекта ChromeOptions для дополнительных настроек браузера
options_chrome = webdriver.ChromeOptions()
# options_chrome.add_argument('--no-sandbox')
# options_chrome.add_argument('--headless')
# options_chrome.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome()
browser.get(URL)

WebDriverWait(browser, 10)

if close_modal(browser):
    browser.save_screenshot("page.png")

if login_btn_press(browser):
    browser.save_screenshot("login.png")

phone_number_press(browser, "934343242")
# selenium_sessions[user_id] = browser

# login_field = browser.find_element(By.ID, "phone-number")
# login_field.click()
#
# login_field.send_keys("934343242")
# browser.save_screenshot("ins_number.png")

    # # element = WebDriverWait(browser, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, "home"))).click()
    # time.sleep(30)
    #
    #
    # # close_modal_window_btn = browser.find_element(By.CSS_SELECTOR, "#app > div.main-view > div.main-container > div > div.mf-modal.show.modal > div.mf-modal-content.md > button")
    # # time.sleep(1)
    # # close_modal_window_btn.click()
    #
    # button_login = browser.find_element(By.CSS_SELECTOR,
    #                                    "#app > div.main-view > div.normal-header.top-header > div.top-header-wrapper > button.mf-button.mf-button-light.sign-in")
    # time.sleep(3)
    # button_login.click()
    #
    # # print(text.text)

    # browser.save_screenshot("page.png")

    # soup = BeautifulSoup(browser.page_source,  'lxml')
    # headings = soup.find('div',  {'class': 'elementor-heading-title'})
    # time.sleep(10)
    # for heading in headings:
    #     print(heading.getText())
