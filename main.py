import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionMiddleware

from core.handlers.basic import startup, shutting_off
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
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%("
               "funcName)s(%(lineno)d) - %(message)s"
    )

    # Сообщения по расписанию
    scheduler.add_job(
        func=alerts_message, trigger='cron',
        hour='07', minute='00',
        start_date=dt.now(), kwargs={'bot': bot}
    )
    scheduler.add_job(
        func=alerts_message, trigger='cron',
        hour='13', minute='00',
        start_date=dt.now(), kwargs={'bot': bot})
    scheduler.add_job(
        func=alerts_message, trigger='cron',
        hour='17', minute='00',
        start_date=dt.now(), kwargs={'bot': bot}
    )

    # Сбор статистики
    scheduler.add_job(
        func=temperature_graph, trigger='cron',
        hour='00', minute='00', start_date=dt.now()
    )
    scheduler.add_job(
        func=save_data, trigger='cron',
        hour='23', minute='58', start_date=dt.now()
    )
    scheduler.add_job(
        func=warning_database, trigger='cron',
        hour='23', minute='59',
        start_date=dt.now(), kwargs={'bot': bot}
    )
    scheduler.add_job(
        func=graph, trigger='interval',
        hours=1, next_run_time=dt.now() + timedelta(seconds=5)
    )

    # Функции для запуска и завершения работы бота
    dp.startup.register(startup)
    dp.shutdown.register(shutting_off)

    # Обработка middlewares
    dp.message.middleware(ChatActionMiddleware())
    dp.callback_query.middleware(ChatActionMiddleware())

    # Обработка сообщений
    dp.message.register(cmd_start, Command(commands=['start']))
    dp.message.register(cmd_help, Command(commands=['help']))
    dp.message.register(cmd_developer, Command(commands=['support']))
    dp.message.register(cmd_manage, Command(commands=['manage']))
    dp.message.register(cmd_message, IsAdmin(), Command('message'))
    dp.message.register(call_alerts_message, IsAdmin(), Command('alerts'))
    dp.message.register(send_graph_admin, IsAdmin(), Command('graph'))
    dp.message.register(upload_database, IsAdmin(), Command(commands=['db']))
    dp.message.register(weather, F.text.lower() == 'погода')
    dp.message.register(second_step_alert, F.text and StateAlerts.subscribe)
    dp.message.register(set_city, F.text and StateSet.city)
    dp.message.register(unknown_message_text, F.text)
    dp.message.register(unknown_message)

    # Обработка callback-ов
    dp.callback_query.register(weather_with_button,
                               F.data.startswith('weather_'))
    dp.callback_query.register(cmd_help, F.data == 'help')
    dp.callback_query.register(city_kb, F.data.startswith('city_'))
    dp.callback_query.register(call_city, F.data.startswith('menu_'))
    dp.callback_query.register(send_graph, F.data.startswith('graph_'))
    dp.callback_query.register(kb_set, F.data.startswith('kb_'), StateSet.city)
    dp.callback_query.register(call_alerts, F.data.startswith('alerts_'))
    try:
        global_init('DataBase.db')
        scheduler.start()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
