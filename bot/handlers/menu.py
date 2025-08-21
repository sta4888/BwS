from aiogram import Router, F
from aiogram.types import Message

menu_router = Router(name="menu router")


@menu_router.message(F.text == "🗳 Голосовать")
async def vote_handler(message: Message):
    await message.answer("🗳 Вы выбрали: Голосовать!")


@menu_router.message(F.text == "💰 Баланс")
async def balance_handler(message: Message):
    await message.answer("💰 Ваш баланс: 0₽")


@menu_router.message(F.text == "📊 Все голоса")
async def all_votes_handler(message: Message):
    await message.answer("📊 Ваши голоса: пока пусто")


@menu_router.message(F.text == "🏦 Вывод средств")
async def withdraw_handler(message: Message):
    await message.answer("🏦 Запрос на вывод средств принят.")
