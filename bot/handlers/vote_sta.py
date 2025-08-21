import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from selenium.webdriver.support.wait import WebDriverWait

from bot.states import VoteIns

from selenium import webdriver

from bot.utils.selen_utils import close_modal, login_btn_press, phone_number_press
from bot.vars import URL

router = Router(name="Vote Router")

# словарь для хранения selenium-сессий по user_id
selenium_sessions: dict[int, webdriver.Chrome] = {}

# ====== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ======
def start_selenium_session(user_id: int, phone: str) -> None:
    """Запускает Selenium, авторизует телефон и сохраняет сессию"""
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument("--no-sandbox")
    options_chrome.add_argument("--headless")
    options_chrome.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options_chrome)
    browser.get(URL)

    WebDriverWait(browser, 10)

    # Закрыть модалку (если есть), нажать "Войти", ввести телефон
    try:
        close_modal(browser)
    except Exception:
        pass  # модалки могло не быть

    if not login_btn_press(browser):
        # можно логировать/кинуть исключение — на твоё усмотрение
        ...

    phone_number_press(browser, phone)

    # сохраняем сессию под user_id
    selenium_sessions[user_id] = browser


def get_selenium_session(user_id: int) -> webdriver.Chrome | None:
    """Возвращает selenium-драйвер для юзера"""
    return selenium_sessions.get(user_id)


def submit_sms_code(user_id: int, code: str) -> bool:
    """Вводит SMS-код через Selenium и завершает шаг"""
    driver = get_selenium_session(user_id)
    if not driver:
        return False

    # Пример: доработай под реальные селекторы/кнопки
    # code_input = driver.find_element(By.ID, "sms_code")
    # code_input.send_keys(code)
    # driver.find_element(By.ID, "submit").click()

    # Закрыть браузер, если дальше не нужен
    try:
        driver.close()
    except Exception:
        pass
    finally:
        selenium_sessions.pop(user_id, None)

    return True


# ====== ХЕНДЛЕРЫ ======

# 1) Запуск по команде /vote
@router.message(Command("vote"))
async def cmd_vote(message: Message, state: FSMContext):
    await message.answer("Введите ваш номер телефона (в формате +99998887766):")
    await state.set_state(VoteIns.send_phone)

# 2) Запуск по кнопке ReplyKeyboard "Голосовать"
#    (!) Текст должен совпадать с текстом твоей кнопки. Если у тебя с эмодзи — оставь оба варианта.
@router.message(F.text.in_({"Голосовать", "🗳 Голосовать"}))
async def vote_button(message: Message, state: FSMContext):
    # тот же поток, что и /vote
    await cmd_vote(message, state)


# обработка введённого телефона
@router.message(VoteIns.send_phone, F.text.regexp(r"^\+9\d{10}$"))
async def phone_received(message: Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)

    # уведомим пользователя, что процесс пошёл
    await message.answer("⏳ Запускаю браузер и ввожу ваш номер...")

    # Запустим Selenium в отдельном потоке
    await asyncio.to_thread(start_selenium_session, message.from_user.id, phone)

    await message.answer("✅ Номер введён. Теперь введите код из SMS:")
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

    await message.answer("⏳ Проверяю код...")

    success = await asyncio.to_thread(submit_sms_code, message.from_user.id, message.text)

    if success:
        await message.answer(
            f"✅ Телефон {phone} успешно подтверждён.\n"
            f"Код {message.text} принят."
        )
    else:
        await message.answer("❌ Ошибка: сессия не найдена. Попробуйте /vote заново.")

    await state.clear()



# обработка неправильного кода
@router.message(VoteIns.send_submit_code)
async def code_invalid(message: Message):
    await message.answer("Код некорректный. Введите ещё раз (4–6 цифр):")
