import asyncio
import logging

from datetime import timedelta, datetime as dt

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Dispatcher, Bot
from aiogram.utils.chat_action import ChatActionMiddleware
from sqlalchemy import URL

from source.settings import settings
from source.middlewares.filters import IsNotPrivate
from source.utils.other import alerts_message, warning_database
from source.database import get_async_engine, create_all_scheme, create_session, Connector
from source.handlers import is_not_private
from source.handlers import message_router, basic_router, callback_router, city_router,\
    admin_router, subscribe_router, transition_router


async def start():
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dispatcher = Dispatcher()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(message)s"
    )
    logging.info(settings)
    postgres_url = URL.create(
        'postgresql+asyncpg',
        username=settings.env.db_username,
        password=settings.env.db_pass,
        host='localhost',
        port=5432,
        database=settings.env.db_name
    )
    engine = get_async_engine(postgres_url)
    connector = Connector(connector=await create_session(engine=engine))
    next_hour = dt.now()+timedelta(minutes=60-dt.now().minute)

    # События по расписанию
    scheduler.add_job(alerts_message, trigger='interval', hours=1,
                      start_date=next_hour.replace(second=0),
                      kwargs={'bot': bot, 'db': connector.connector})

    scheduler.add_job(warning_database, trigger='cron',
                      hour='23', minute='59', start_date=dt.now(),
                      kwargs={'bot': bot})

    # middlewares
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

    await create_all_scheme(engine)
    logging.info(f"Подключено к базе данных {postgres_url}")
    try:
        scheduler.start()
        await dispatcher.start_polling(
            bot, connector=connector, scheduler=scheduler,
        )
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
