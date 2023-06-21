from aiogram import Router, flags, Bot
from aiogram.exceptions import TelegramNetworkError
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from core.middlewares.filters import IsAdmin

from core.utils.other import alerts_message, get_weather_for_cities
from core.database.Connector import Connector

router = Router()


@router.message(Command(commands='message'), IsAdmin())
async def cmd_message(message: Message, bot: Bot, connector: Connector):
    count_right = 0
    count_left = 0
    for user in await connector.all_users():
        try:
            await get_weather_for_cities(user_id=user, bot=bot, chat_id=user)
            await connector.update_status(message.from_user.id)
            count_right += 1
        except Exception:
            count_left += 1
            await connector.update_status(message.from_user.id, 'banned')
    await message.answer(
        text="Рассылка завершена\n\r"
             f"Удачных сообщений: <b>{count_right}</b>\n\r"
             f"Не удачных: <b>{count_left}</b>\n\r"
             f"Всего сообщений: <b>{count_left + count_right}</b>",
        parse_mode='html'
    )


@router.message(Command('alerts'), IsAdmin())
async def call_alerts_message(message: Message, bot: Bot):
    await message.answer('Начинаю рассылку')
    await alerts_message(bot=bot)


@router.message(Command(commands=['db']), IsAdmin())
@flags.chat_action('upload_document')
async def upload_database(message: Message):
    try:
        await message.answer_document(
            document=FSInputFile(f'core\\DataBase.db'),
        )
    except TelegramNetworkError:
        await message.answer('Что-то пошло не так')


@router.message(Command('log'), IsAdmin())
async def send_log(msg: Message):
    try:
        await msg.answer_document(document=FSInputFile(r'core\log.log'))
    except TelegramNetworkError:
        await msg.answer('Что-то пошло не так')
