from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot


from core.handlers.basic import set_default_commands
from core.keyboards.inline import mark, menu, admin, weather_btn
from core.keyboards.reply import get_weather_button
from core.utils.connect_db import User
from core.utils.other import get_weather
from core.utils.session_db import create_session

router = Router()


@router.message(Command(commands=['start']))
async def cmd_start(message: Message, bot: Bot):
    await set_default_commands(bot)
    with create_session() as db:
        users = [user[0] for user in db.query(User.id).all()]
        if message.from_user.id in users:
            await message.answer(
                f'Привет, ***{message.from_user.first_name}*** \U0001F609 !\n'
                f'Я Telegram-бот для получения погоды в любом регионе. '
                f'Для получения всех команд, которые я понимаю, нажмите "help".'
                f'\nИли пропишите команду /help.\n',
                parse_mode='Markdown',
                reply_markup=mark())
            await bot.send_message(
                message.chat.id,
                f'Вижу ты тут впервые, '
                f'напишите "/manage" для того что бы установить регион'
                f' для получения погоды.'
                f'\nТак же ты можешь написать любой регион, '
                f'а я отправлю погоду в этом регионе \U000026C5',
                parse_mode=''
            )
            db.add(User(
                id=message.from_user.id,
                username=message.from_user.username,
                active=True
            ))
        else:
            await bot.send_message(
                message.chat.id,
                f'Привет, ***{message.from_user.first_name}*** \U0001F609!\n'
                f'Я тебя помню!\n'
                f'Нажми "help" для ознакомления с командами.\n'
                f'Напиши регион для получения погоды \U000026C5',
                reply_markup=mark(),
                parse_mode='Markdown')
            await message.answer(
                'Если у тебя уже выставлен регион просто нажми "Погода"',
                reply_markup=get_weather_button())
            db.query(User).where(User.id == message.from_user.id).update(
                {User.active: True}
            )
        db.commit()


@router.callback_query(F.data == 'help')
@router.message(Command(commands=['help']))
async def cmd_help(message: [Message, CallbackQuery], bot: Bot):
    text = f'Я понимаю эти команды:\n'\
           f'/start\n/help\n/developer\n/manage\n'\
           f'Для получения погоды напишите желаемый регион.\n'\
           f'Для получения погоды в установленном регионе нажми "погода"'
    if type(message) is CallbackQuery:
        await message.answer()
        await bot.send_message(
            message.message.chat.id,
            text=text,
            parse_mode='',
            reply_markup=get_weather_button())
    elif type(message) is Message:
        await bot.send_message(
            message.chat.id,
            text=text,
            parse_mode='',
            reply_markup=get_weather_button())
    with create_session() as db:
        db.query(User).where(User.id == int(message.from_user.id)).update(
            {User.active: True})
        db.commit()


@router.message(Command(commands=['manage']))
async def cmd_manage(message: Message):
    await message.answer(text=f'Выберите опцию:', reply_markup=menu())


@router.message(Command(commands=['support']))
async def cmd_developer(message: Message, bot: Bot):
    await bot.send_message(
        message.chat.id,
        text='<strong>@w1thoutiq</strong>',
        reply_markup=admin(), parse_mode='HTML'
    )


@router.message(F.text.lower() == 'погода')
async def weather(message: Message):
    try:
        with create_session() as db:
            cities = db.query(User.city).where(
                User.id == int(message.from_user.id)).first()[0].split(', ')
        await message.answer(text='Для какого региона показать погоду?',
                             reply_markup=weather_btn(cities))
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
