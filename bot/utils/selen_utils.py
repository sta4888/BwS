import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def close_modal(driver) -> bool:
    print("close_modal")
    try:
        time.sleep(3)
        # находим элемент, по которому надо кликнуть
        element = driver.find_element(By.CSS_SELECTOR, ".mf-modal-close")

        # создаем объект действий
        actions = ActionChains(driver)

        # наведение мышки и клик
        actions.move_to_element(element).click().perform()

        time.sleep(2)
        driver.save_screenshot("screens/"+"page.png")
    except Exception as e:
        print(e)
        return False
    return True

def login_btn_press(driver) -> bool:
    print("login_btn_press")
    try:
        button_login = driver.find_element(
            By.CSS_SELECTOR,
            "#app > div.main-view > div.normal-header.top-header > "
            "div.top-header-wrapper > button.mf-button.mf-button-light.sign-in"
        )

        button_login.click()
        time.sleep(3)
        driver.save_screenshot("screens/"+"login.png")
    except Exception as e:
        print(e)
        return False
    return True

def phone_number_press(driver, phone):
    print("phone_number_press")
    time.sleep(3)
    try:
        login_field = driver.find_element(By.ID, "phone-number")
        login_field.click()

        login_field.send_keys(phone[-9:])
        driver.save_screenshot("screens/"+phone[-9:]+"ins_number.png")
    except Exception as e:
        print(e)