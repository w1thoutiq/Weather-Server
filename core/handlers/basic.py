from aiogram import Bot, Router
from aiogram.types import BotCommand, BotCommandScopeDefault, Message


router = Router()


@router.startup()
async def set_default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description='Запуск бота'),
            BotCommand(command='manage', description='Управление'),
            BotCommand(command='help', description='Все то, что умеет бот'),
            BotCommand(command='support', description='Решение проблем'),
        ], scope=BotCommandScopeDefault())


async def is_not_private(msg: Message):
    await msg.answer('Это не личные сообщения')
