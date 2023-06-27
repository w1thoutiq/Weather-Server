import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Dispatcher, Bot

from source.handlers.router import connect_handlers
from source.settings import settings
from source.database import create_session, Connector, connect_database


async def start():
    bot = Bot(token=settings.bot.token, parse_mode='HTML')
    dispatcher = Dispatcher()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(message)s"
    )
    logging.info(settings.bot)
    connector = Connector(connector=await create_session())
    await connect_database()
    await connect_handlers(dispatcher, scheduler, bot, connector.connector)
    try:
        scheduler.start()
        await dispatcher.start_polling(
            bot, connector=connector, scheduler=scheduler,
        )
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
