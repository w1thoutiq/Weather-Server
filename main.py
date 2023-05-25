import asyncio
import logging
from datetime import timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Dispatcher, F, Bot
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionMiddleware

from core.handlers.basic import startup, shutting_off
from core.utils.simple_func import alerts_message
from core.handlers.callback import *
from core.handlers.message import *
from core.settings import settings
from core.utils.states import *
from core.middlewares.filters import IsAdmin
from core.utils.graph import *


async def start():
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    # Сообщения по расписанию
    scheduler.add_job(alerts_message, trigger='cron', hour='07', minute='00', start_date=dt.now(), kwargs={'bot': bot})
    scheduler.add_job(alerts_message, trigger='cron', hour='13', minute='00', start_date=dt.now(), kwargs={'bot': bot})
    scheduler.add_job(alerts_message, trigger='cron', hour='17', minute='00', start_date=dt.now(), kwargs={'bot': bot})

    # Сбор статистики
    scheduler.add_job(temperature_graph, trigger='cron', hour='00', minute='00', start_date=dt.now())
    scheduler.add_job(save_data, trigger='cron', hour='23', minute='57', start_date=dt.now())
    scheduler.add_job(warning_database, trigger='cron', hour='23', minute='58', start_date=dt.now(),
                      kwargs={'bot': bot})
    scheduler.add_job(graph, trigger='interval', hours=1, next_run_time=dt.now()+timedelta(seconds=5))

    # Функции для запуска и завершения работы бота
    dp.startup.register(startup)
    dp.shutdown.register(shutting_off)

    # Обработка middlewares
    dp.message.middleware(ChatActionMiddleware())
    dp.callback_query.middleware(ChatActionMiddleware())

    # Обработка сообщений
    dp.message.register(cmd_start, Command(commands=['start']))
    dp.message.register(cmd_help, Command(commands=['help']))
    dp.message.register(cmd_developer, Command(commands=['developer']))
    dp.message.register(cmd_manage, Command(commands=['manage']))
    dp.message.register(cmd_message, IsAdmin() and Command(commands=['message']))
    dp.message.register(call_alerts_message, IsAdmin() and Command(commands=['alerts']))
    dp.message.register(send_graph_admin, IsAdmin() and Command(commands=['graph']))
    dp.message.register(upload_database, IsAdmin() and Command(commands=['db']))
    dp.message.register(weather, F.text.lower() == 'погода')
    dp.message.register(second_step_alert, F.text and StateAlerts.subscribe)
    dp.message.register(set_city, F.text and StateSet.city)
    dp.message.register(unknown_message_text, F.text)
    dp.message.register(unknown_message)

    # Обработка callback-ов
    dp.callback_query.register(weather_with_button, F.data.startswith('weather_'))
    dp.callback_query.register(cmd_help, F.data == 'help')
    dp.callback_query.register(city_kb, F.data.startswith('city_'))
    dp.callback_query.register(call_city, F.data.startswith('menu_'))
    dp.callback_query.register(send_graph, F.data.startswith('graph_'))
    dp.callback_query.register(kb_set, F.data.startswith('kb_') and StateSet.city)
    dp.callback_query.register(call_alerts, F.data.startswith('alerts_'))
    try:
        global_init('DataBase.db')
        scheduler.start()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
