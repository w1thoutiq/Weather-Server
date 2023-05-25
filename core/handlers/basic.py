from aiogram import Bot
from aiogram.exceptions import TelegramNetworkError
from aiogram.types import BotCommand, BotCommandScopeDefault, FSInputFile
from core.settings import settings


async def startup(bot: Bot):
    await set_default_commands(bot)
    await bot.send_message(
        chat_id=settings.bots.admin_id,
        text="Бот запущен!",
        disable_notification=True,
    )


async def shutting_off(bot: Bot):
    await bot.send_message(
        chat_id=settings.bots.admin_id,
        text="Бот выключен!",
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
            BotCommand(command='developer', description='Посмотреть разработчика'),
        ],
        scope=BotCommandScopeDefault(), )
