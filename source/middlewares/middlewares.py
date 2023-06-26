# import logging
from typing import Dict, Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from aiogram.exceptions import TelegramForbiddenError as BotBlocked


from source.database.connector import Connector


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        print(data)
        data['scheduler'] = self.scheduler
        return await handler(event, data)


class ConnectorMiddleware(BaseMiddleware):
    def __init__(self, connector: Connector):
        self.connector = connector

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['connector'] = self.connector
        return await handler(event, data)

