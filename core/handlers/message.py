from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from core.utils.simple_func import *
from core.keyboards.inline import *
from core.keyboards.reply import *
from core.utils.session_db import *
from core.utils.connect_db import *
from core.handlers.basic import set_default_commands
from core.utils.graph import admin_graph


@flags.chat_action('typing')
# Функция для обработки /start
async def cmd_start(message: Message, bot: Bot):
    await set_default_commands(bot)
    with create_session() as db:
        users = [user[0] for user in db.query(User.id).all()]
        if message.from_user.id not in users:
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


@flags.chat_action('typing')
# Функция для обработки /help
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


@flags.chat_action('typing')
# Функция для обработки /manage
async def cmd_manage(message: Message):
    await message.answer(text=f'Выберите опцию:', reply_markup=menu())


@flags.chat_action('typing')
# Функция для обработки /developer
async def cmd_developer(message: Message, bot: Bot):
    await bot.send_message(
        message.chat.id,
        text='<strong>@w1thoutiq</strong>',
        reply_markup=admin(), parse_mode='HTML'
    )


@flags.chat_action('typing')
# Функция для обработки /message
async def cmd_message(message: Message, bot: Bot):
    count_right = 0
    count_left = 0
    with create_session() as db:
        users = [int(user[0]) for user in db.query(User.id).all()]
        for user in users:
            try:
                await get_weather_for_cities(
                    user_id=user, bot=bot, chat_id=user
                )
                if db.query(User.active).where(User.id == user) is False:
                    db.query(User).where(User.id == user).update(
                        {User.active: True})
                count_right += 1
            except TelegramBadRequest:
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


@flags.chat_action('typing')
# Функция для обработки текста "Погода"
async def weather(message: Message):
    with create_session() as db:
        cities = db.query(User.city).where(
            User.id == int(message.from_user.id)).first()[0].split(', ')
    await message.answer(text='Для какого региона показать погоду?',
                         reply_markup=weather_btn(cities))


@flags.chat_action('typing')
async def call_alerts_message(message: Message, bot: Bot):
    await message.answer('Начинаю рассылку')
    await alerts_message(bot=bot)


@flags.chat_action('typing')
# state=StateAlerts.subscribe
async def second_step_alert(message: Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer(f'Главное меню', reply_markup=menu())
    else:
        with create_session() as db:
            city = message.text.capitalize()
            try:  # Обработка ошибки если такого региона не существует
                if get_weather(city) is None:
                    raise ValueError
                if db.query(Alert).where(
                        Alert.id == int(message.from_user.id)).first() is None:
                    db.add(Alert(
                        id=message.from_user.id,
                        username=message.from_user.username,
                        city=city
                    ))
                else:
                    db.query(Alert).where(
                        Alert.id == int(message.from_user.id)).update(
                        {
                            Alert.id: message.from_user.id,
                            Alert.city: city,
                            Alert.username: message.from_user.username
                        }
                    )
                data = await state.get_data()
                call = data.get('call')
                await call.message.edit_text(
                    text='Вы подписаны на рассылку 🎉',
                    reply_markup=menu()
                )
                await state.clear()
            except ValueError:
                await message.reply(f'Что-то пошло не так! \U0001F915'
                                    f'\nНапишите "отмена", если передумали',
                                    reply_markup=cancel())
            finally:
                db.commit()
                await message.delete()


@flags.chat_action('typing')
# state=StateSet.city
async def set_city(message: Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer(f'Главное меню', reply_markup=menu())
    else:
        city = message.text.capitalize()
        try:  # Обработка ошибки если такого региона не существует
            if get_weather(city) is None:
                raise ValueError
            await state.update_data(city=city)
            await message.answer(f'Что ты хочешь сделать с этим регионом?',
                                 reply_markup=add_city_menu()
                                 )
        except ValueError:
            await message.reply(
                f'Что-то пошло не так! \U0001F915'
                f'\nНапишите "отмена", если передумали',
                reply_markup=cancel()
                                )


@flags.chat_action('typing')
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


@flags.chat_action('upload_photo')
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


@flags.chat_action('upload_document')
async def upload_database(message: Message):
    try:
        await message.answer_document(
            document=FSInputFile(f'DataBase.db'),
            caption=f'Ваша база данных'
        )
    except TelegramNetworkError:
        await message.answer('Что-то пошло не так')


@flags.chat_action('typing')
# Обработка любого типа сообщений, что-бы избежать лишних ошибок
async def unknown_message(message: Message):
    await message.reply(f'Я не знаю что с этим делать, но напоминаю,\n'
                        f'что вы можете использовать команду /help',
                        parse_mode='Markdown', reply_markup=mark())
