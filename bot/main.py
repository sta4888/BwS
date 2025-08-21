import asyncio

from aiogram import Bot, Dispatcher

from bot.handlers import get_routers
from bot.vars import BOT_TOKEN


async def main():

    dp = Dispatcher()
    dp.include_routers(*get_routers())

    bot = Bot(token=BOT_TOKEN)

    # Получаем данные о боте
    me = await bot.get_me()
    print(f"Бот запущен: {me.first_name} (@{me.username})")

    print("Starting polling...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())