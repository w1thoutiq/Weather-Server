import asyncio
import logging

from datetime import timedelta, datetime as dt

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Dispatcher, Bot
from aiogram.utils.chat_action import ChatActionMiddleware

from core.settings import settings
from core.middlewares.filters import IsNotPrivate
from core.utils.other import alerts_message, warning_database
from core.database.__all__ import global_init
from core.handlers.message import router as message_router
from core.handlers.callback import router as callback_router
from core.middlewares.utils import router as transition_router
from core.handlers.basic import router as basic_router, is_not_private
from core.handlers.city import router as city_router
from core.handlers.admin import router as admin_router
from core.handlers.subscribe import router as subscribe_router
from core.middlewares.middlewares import SchedulerMiddleware, \
    ConnectorMiddleware
from core.database.Connector import Connector


async def start():
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dispatcher = Dispatcher()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(message)s"
    )
    logging.info(settings)

    next_hour = dt.now()+timedelta(minutes=60-dt.now().minute)

    # События по расписанию
    scheduler.add_job(alerts_message, trigger='interval', hours=1,
                      start_date=next_hour.replace(second=0),
                      kwargs={'bot': bot})

    scheduler.add_job(warning_database, trigger='date',
                      run_date=dt.now(),#, hour='23', minute='59'
                      kwargs={'bot': bot})

    # Обработка middlewares
    dispatcher.update.middleware.register(ConnectorMiddleware(Connector()))
    dispatcher.update.middleware.register(SchedulerMiddleware(scheduler))
    dispatcher.callback_query.middleware.register(ChatActionMiddleware())
    dispatcher.message.middleware.register(ChatActionMiddleware())

    # Подключение router'ов
    dispatcher.message.register(is_not_private, IsNotPrivate())
    dispatcher.include_router(admin_router)
    dispatcher.include_router(city_router)
    dispatcher.include_router(subscribe_router)
    dispatcher.include_router(callback_router)
    dispatcher.include_router(basic_router)
    dispatcher.include_router(transition_router)
    dispatcher.include_router(message_router)

    try:
        global_init('core/DataBase.db')
        scheduler.start()
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
