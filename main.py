import asyncio
import logging

from datetime import timedelta, datetime as dt
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Dispatcher, Bot
from aiogram.utils.chat_action import ChatActionMiddleware

from core.handlers.basic import startup, shutting_off
from core.settings import settings
from core.utils.other import alerts_message, warning_database
from core.utils.session_db import global_init
from core.handlers.message import router as message_router
from core.handlers.callback import router as callback_router


async def start():
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(message)s"
    )
    logging.info(settings.bots)

    # Сообщения по расписанию
    scheduler.add_job(
        func=alerts_message,
        trigger='interval',
        hours=1,
        next_run_time=(dt.now()+timedelta(minutes=60-dt.now().minute)).replace(second=0, microsecond=0),
        kwargs={'bot': bot}
    )
    # Сбор статистики
    scheduler.add_job(func=warning_database, trigger='cron', hour='23', minute='59', start_date=dt.now(), kwargs={'bot': bot})

    # Функции для запуска и завершения работы бота
    dp.startup.register(startup)
    dp.shutdown.register(shutting_off)

    # Обработка middlewares
    dp.message.middleware(ChatActionMiddleware())
    dp.callback_query.middleware(ChatActionMiddleware())

    # Подключение router'ов
    dp.include_router(message_router)
    dp.include_router(callback_router)

    try:
        global_init('DataBase.db')
        scheduler.start()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
