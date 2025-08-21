from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from selenium.webdriver.support.wait import WebDriverWait

from bot.states import VoteIns

from selenium import webdriver
from selenium.webdriver.common.by import By

from bot.utils.selen_utils import close_modal, login_btn_press, phone_number_press
from bot.vars import URL

router = Router(name="Vote Router")

# словарь для хранения selenium-сессий по user_id
selenium_sessions = {}


# ====== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ======
def start_selenium_session(user_id: int, phone: str):
    """Запускает Selenium, авторизует телефон и сохраняет сессию"""
    browser = webdriver.Chrome()
    browser.get(URL)

    WebDriverWait(browser, 10)

    if not close_modal(browser):
        ...

    if not login_btn_press(browser):
        ...

    phone_number_press(browser, phone)
    selenium_sessions[user_id] = browser


def get_selenium_session(user_id: int):
    """Возвращает selenium-драйвер для юзера"""
    return selenium_sessions.get(user_id)


def submit_sms_code(user_id: int, code: str):
    """Вводит SMS-код через Selenium"""
    driver = get_selenium_session(user_id)
    if not driver:
        return False

    # code_input = driver.find_element(By.ID, "sms_code")
    # code_input.send_keys(code)
    # driver.find_element(By.ID, "submit").click()
    driver.close()
    return True


# ====== ХЕНДЛЕРЫ ======

# старт процесса ввода телефона
@router.message(Command("vote"))
async def cmd_vote(message: Message, state: FSMContext):
    await message.answer("Введите ваш номер телефона (в формате +99998887766):")
    await state.set_state(VoteIns.send_phone)


# обработка введённого телефона
@router.message(VoteIns.send_phone, F.text.regexp(r"^\+9\d{10}$"))
async def phone_received(message: Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)

    # запускаем Selenium
    start_selenium_session(message.from_user.id, phone)

    await message.answer("Спасибо! Теперь введите код из SMS:")
    await state.set_state(VoteIns.send_submit_code)


# обработка некорректного номера
@router.message(VoteIns.send_phone)
async def phone_invalid(message: Message):
    await message.answer(
        "Номер телефона некорректный.\n"
        "Введите в формате +99998887766:"
    )


# обработка введённого кода
@router.message(VoteIns.send_submit_code, F.text.regexp(r"^\d{4,6}$"))
async def code_received(message: Message, state: FSMContext):
    user_data = await state.get_data()
    phone = user_data.get("phone")

    # передаём код в Selenium
    success = submit_sms_code(message.from_user.id, message.text)

    if success:
        await message.answer(
            f"Телефон {phone} успешно подтверждён ✅\n"
            f"Код {message.text} принят."
        )
    else:
        await message.answer("Ошибка: сессия не найдена. Попробуйте /vote заново.")

    await state.clear()


# обработка неправильного кода
@router.message(VoteIns.send_submit_code)
async def code_invalid(message: Message):
    await message.answer("Код некорректный. Введите ещё раз (4–6 цифр):")
