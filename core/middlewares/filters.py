from aiogram.filters import BaseFilter
from aiogram.types import Message
from core.settings import settings


class IsAdmin(BaseFilter):
    def __call__(self, message: Message) -> bool:
        match message:
            case message if settings.bots.admin_id == message.from_user.id:
                return True
            case message if settings.bots.admin_id != message.from_user.id:
                return False
            case _:
                print('Что-то не так в фильтре')
                return False
