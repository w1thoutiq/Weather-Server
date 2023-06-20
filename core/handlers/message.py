from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot
from sqlalchemy.exc import IntegrityError

from core.keyboards.inline import mark, menu, admin
from core.keyboards.reply import get_weather_button
from core.utils.other import get_weather
from core.database.Connector import Connector


router = Router()


@router.message(Command(commands=['start']))
async def cmd_start(message: Message, connector: Connector):
    try:
        await connector.add_in_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            status='member'
        )
    except IntegrityError:
        await connector.update_status(message.from_user.id, 'member')
    finally:
        await message.answer(
            f'Привет, ***{message.from_user.first_name}*** 🖐 !\n'
            f'Я Telegram-бот для получения погоды в любом регионе. '
            f'Для получения всех команд, которые я понимаю, пропишите команду /help.',
            parse_mode='Markdown',
            reply_markup=mark())
        await message.answer(
            f'Меню \U000026C5',
            reply_markup=menu(),
            disable_notification=False
        )


@router.callback_query(F.data == 'help')
@router.message(Command(commands=['help']))
async def cmd_help(message: Message | CallbackQuery, bot: Bot, connector: Connector):
    text = f'Я понимаю эти команды:\n'\
           f'/start\n/help\n/support\n/manage\n'\
           f'Для получения погоды напишите желаемый регион.\n'\
           f'Для получения погоды в установленном регионе нажми "погода"'
    await bot.send_message(message.from_user.id, text=text,
                           reply_markup=get_weather_button())
    await connector.update_status(message.from_user.id, 'member')
    try:
        await message.answer()
    except Exception:
        pass


@router.message(Command(commands=['manage']))
async def cmd_manage(message: Message):
    await message.answer(text=f'Меню:', reply_markup=menu())


@router.message(Command(commands=['support']))
async def cmd_developer(message: Message, bot: Bot):
    await bot.send_message(
        message.chat.id,
        text='<strong>@w1thoutiq</strong>',
        reply_markup=admin(), parse_mode='HTML'
    )


@router.message(F.text.lower() == 'погода')
async def weather(message: Message, connector: Connector):
    try:
        city = await connector.alert_city(message.from_user.id)
        await message.answer(text=get_weather(city))
    except TypeError:
        await message.answer("Нет установленных регионов")


@router.message(F.text)
# Обработка любого текста, если есть город, тогда вернет погоду пользователю
async def unknown_message_text(message: Message):
    try:
        city = message.text.capitalize()
        await message.answer(
            text=get_weather(city),
            parse_mode='HTML'
        )
    except Exception:
        await message.reply(f'\U0001F915 Страна или регион указан неверно!')


@router.message()
# Обработка любого типа сообщений, что-бы избежать лишних ошибок
async def unknown_message(message: Message):
    await message.reply(f'Я не знаю что с этим делать, но напоминаю,\n'
                        f'что вы можете использовать команду /help',
                        parse_mode='Markdown', reply_markup=mark())
