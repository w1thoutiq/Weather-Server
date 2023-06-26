from aiogram.exceptions import TelegramNetworkError
from requests import get
from aiogram import Bot, flags
from aiogram.types import CallbackQuery, FSInputFile
from datetime import datetime, timedelta

from sqlalchemy import select

from source.settings import settings
from source.keyboards.inline import *
from source.keyboards.reply import *
from source.database.connector import Connector
from source.database import User, create_session, Alert


async def warning_database(bot: Bot):
    try:
        await bot.send_document(
            chat_id=settings.bots.admin_id,
            document=FSInputFile(f'core/DataBase.db'),
            caption=f'{datetime.now().date()}',
            disable_notification=True
        )
        await bot.send_document(
            chat_id=settings.bots.admin_id,
            document=FSInputFile(f'core/log.log'),
            disable_notification=True
        )
    except TelegramNetworkError:
        pass


@flags.chat_action("typing")
# Обычный вывод установленного города
async def my_city(call: CallbackQuery, bot: Bot, connector: Connector):
    try:
        city = await connector.cities_of_user(call.from_user.id)
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=f'Установленные регионы:',
            reply_markup=weather_btn(city)
        )
    except AttributeError:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=f'У вас нету установленных регионов'
        )


@flags.chat_action("typing")
async def get_weather_for_cities(user_id: int, bot: Bot, chat_id: int):
    with create_session() as db:
        cities = await db.execute(
            select(User.city).where(User.telegram_id == user_id))
        cities = cities.first()[0].split('\n')
    if cities == ['']:
        return await bot.send_message(
            chat_id=chat_id,
            text='Сначала установи регионы'
        )
    if '' in cities:
        cities.remove('')
    for city in cities:
        await bot.send_message(
            chat_id=chat_id,
            text=get_weather(city),
            parse_mode='HTML',
            reply_markup=get_weather_button(),
            disable_notification=True
        )
    return


def get_weather(city, for_graph=False, timezone: bool = False):
    try:
        url = 'https://api.openweathermap.org/data/2.5/weather'
        api_of_weather = '352c751a80237a51813f0ae93d864822'
        params = {'APPID': api_of_weather,
                  'q': city,
                  'units': 'metric',
                  'lang': 'ru'}
        result = get(url, params=params).json()
        info = result['main']['temp'], result['main']['feels_like'],\
            result['weather'][0]['description'], result['name']
        if timezone:
            return result.get('timezone')
        if for_graph is True:
            return info[0]
        message_text = f'Погода в регионе <strong>{info[3]}</strong>:\n' \
                       f'<em><strong>{info[0]} °C, ' \
                       f'ощущается как {info[1]}°C, {info[2]}</strong></em>'
        return message_text
    except KeyError:
        return


@flags.chat_action("typing")
async def alerts_message(bot: Bot, db):
    try:
        async with db() as db:
            async with db.begin():
                users = await db.execute(select(Alert.telegram_id))
                users = users.fetchall()
                users = [int(user[0]) for user in users]
                for user in users:
                    try:
                        city = await db.execute(select(Alert.city).where(Alert.telegram_id == user))
                        city = city.first()[0]
                        timezone = db.execute(select(Alert.timezone).where(Alert.telegram_id == user))
                        timezone = timezone.first()[0]
                        if ((datetime.now()-timedelta(seconds=10800)) + timedelta(seconds=timezone)).hour in [7, 13, 17]:
                            await bot.send_message(
                                chat_id=user,
                                text=get_weather(city),
                                parse_mode='HTML'
                            )
                    except Exception:
                        pass
                await db.commit()
    except Exception:
        pass
