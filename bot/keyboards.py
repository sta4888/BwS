from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Создаем кнопки
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🗳 Голосовать")],
        [KeyboardButton(text="💰 Баланс"), KeyboardButton(text="📊 Все голоса")],
        [KeyboardButton(text="🏦 Вывод средств")]
    ],
    resize_keyboard=True,   # чтобы клавиатура подгонялась под экран
    one_time_keyboard=False # чтобы не скрывалась после нажатия
)
