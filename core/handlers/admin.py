from datetime import datetime

from aiogram import Router, flags, Bot
from aiogram.exceptions import TelegramNetworkError
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from core.utils.graph import admin_graph
from core.middlewares.filters import IsAdmin

from core.utils.connect_db import User
from core.utils.other import alerts_message, get_weather_for_cities
from core.utils.session_db import create_session


router = Router()


@router.message(IsAdmin(), Command(commands='message'))
async def cmd_message(message: Message, bot: Bot):
    count_right = 0
    count_left = 0
    with create_session() as db:
        users = [int(user[0]) for user in db.query(User.id).all()]
        for user in users:
            try:
                await get_weather_for_cities(user_id=user, bot=bot, chat_id=user)
                if db.query(User.active).where(User.id == user) is False:
                    db.query(User).where(User.id == user).update(
                        {User.active: True})
                count_right += 1
            except Exception:
                count_left += 1
                db.query(User).where(User.id == user).update(
                    {User.active: False})
        await message.answer(
            text="Рассылка завершена\n\r"
                 f"Удачных сообщений: <b>{count_right}</b>\n\r"
                 f"Не удачных: <b>{count_left}</b>\n\r"
                 f"Всего сообщений: <b>{count_left + count_right}</b>",
            parse_mode='html'
        )


@router.message(IsAdmin(), Command('alerts'))
async def call_alerts_message(message: Message, bot: Bot):
    await message.answer('Начинаю рассылку')
    await alerts_message(bot=bot)


@router.message(IsAdmin(), Command('graph'))
async def send_graph_admin(message: Message, bot: Bot):
    city = message.text[7::].capitalize()
    admin_graph(city)
    try:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=FSInputFile(f'Graph\\{city}\\{datetime.now().date()}.png'),
            caption=f'График погоды города - <b>{city}</b> за'
                    f' <b>{datetime.now().date()}</b>'
        )
    except TelegramNetworkError:
        await message.answer('График еще не готов ☠')


@router.message(IsAdmin(), Command(commands=['db']))
@flags.chat_action('upload_document')
async def upload_database(message: Message):
    try:
        await message.answer_document(
            document=FSInputFile(f'DataBase.db'),
        )
    except TelegramNetworkError:
        await message.answer('Что-то пошло не так')
