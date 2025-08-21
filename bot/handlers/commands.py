from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards import main_keyboard

router = Router(name="commands router")


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот 😎 Выбери действие:",
        reply_markup=main_keyboard
    )


