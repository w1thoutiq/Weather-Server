from logging import info, error
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram import Router
from aiogram.types import ChatMemberUpdated

from aiogram.exceptions import TelegramForbiddenError,\
    TelegramBadRequest

from core.database.Connector import Connector

router = Router()


@router.errors()
async def error_handler(update, event_from_user):
    user = event_from_user.id
    username = event_from_user.username
    if type(update.exception) is TelegramForbiddenError or \
            type(update.exception) is TelegramBadRequest:
        await Connector().update_status(user=user, status='blocked')
        error(f"Бот заблокирован у {username}")
        print(f"Бот заблокирован у {username}",
              file=open('core/log.log', mode='a+', encoding='utf-8'))
    else:
        error(f"Не известная ошибка {update.exception}")
        print(f"Не известная ошибка {update.exception}",
              file=open('core/log.log', mode='a+', encoding='utf-8'))


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, connector: Connector):
    await connector.update_status(event.from_user.id, status="banned")
    info(f'Пользователь {event.from_user.username} заблокировал бота')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, connector: Connector):
    await connector.update_status(event.from_user.id, status='member')
    info(f'Пользователь {event.from_user.username} разблокировал бота')
