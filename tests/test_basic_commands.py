from datetime import datetime

import pytest
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Update, Chat, User, Message

@pytest.mark.asyncio
async def test_cmd_start(dp, bot):                           # [1]
    bot.add_result_for(                                      # [2]
        method=SendMessage,
        ok=True,
        # result сейчас можно пропустить
    )
    chat = Chat(id=1234567, type=ChatType.PRIVATE)           # [3]
    user = User(id=1234567, is_bot=False, first_name="User") # [3]
    message = Message(                                       # [3]
        message_id=1,
        chat=chat,
        from_user=user,
        text="/start",
        date=datetime.now()
    )
    result = await dp.feed_update(                      # [4]
        bot,
        Update(message=message, update_id=1)
    )
    assert result is not UNHANDLED                      # [5]
    outgoing_message: TelegramType = bot.get_request()  # [6]
    assert isinstance(outgoing_message, SendMessage)    # [7]
    assert outgoing_message.text == "Hello"           # [8]



# проверка пользователя на введенный номер телефона
@pytest.mark.asyncio
async def test_phone_input(dp, bot):
    # ожидаем, что бот отправит сообщение "Номер принят"
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )

    chat = Chat(id=999, type=ChatType.PRIVATE)
    user = User(id=999, is_bot=False, first_name="Tester")

    # имитация ввода пользователем номера
    message = Message(
        message_id=42,
        chat=chat,
        from_user=user,
        text="+79998887766",
        date=datetime.now()
    )

    result = await dp.feed_update(
        bot,
        Update(message=message, update_id=42)
    )

    # проверка, что апдейт обработан
    assert result is not UNHANDLED

    # достаём, что бот реально хотел отправить
    outgoing: TelegramType = bot.get_request()
    assert isinstance(outgoing, SendMessage)
    assert "Номер принят" in outgoing.text
# проверка соответствия номера телефона
# проверка соответствия номера телефона