from aiogram.filters import BaseFilter
from aiogram.types import Message
from source.settings import settings


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == settings.bots.admin_id


class IsNotPrivate(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not (message.chat.type == 'private')
