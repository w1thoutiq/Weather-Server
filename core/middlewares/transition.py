from logging import info
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram import Router
from aiogram.types import ChatMemberUpdated

from core.utils.connect_db import update_status

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    await update_status(event.from_user.id, False)
    info(f'Пользователь {event.from_user.username} заблокировал бота')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated):
    await update_status(event.from_user.id, True)
    info(f'Пользователь {event.from_user.username} разблокировал бота')
