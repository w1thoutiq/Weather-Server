from aiogram import Bot, Router
from aiogram.exceptions import TelegramNetworkError
from aiogram.types import BotCommand, BotCommandScopeDefault, FSInputFile

from core.settings import settings


router = Router()


@router.startup()
async def startup(bot: Bot):
    await set_default_commands(bot)
    await bot.send_message(
        chat_id=settings.bots.admin_id,
        text="Бот запущен!",
        disable_notification=True,
    )


@router.shutdown()
async def shutting_off(bot: Bot):
    await bot.send_message(
        chat_id=settings.bots.admin_id,
        text="Бот выключен!",
        disable_notification=True
    )
    try:
        await bot.send_document(
            chat_id=settings.bots.admin_id,
            document=FSInputFile(f'DataBase.db'),
            caption=f'Аварийная база данных'
        )
    except TelegramNetworkError:
        await bot.send_message(
            chat_id=settings.bots.admin_id,
            text='База данных не отправилась'
        )


async def set_default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description='Запуск бота'),
            BotCommand(command='manage', description='Управление'),
            BotCommand(command='help', description='Все то, что умеет бот'),
            BotCommand(command='support', description='Решение проблем'),
        ], scope=BotCommandScopeDefault(), )
