from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start', description='Старт'
        ),
        BotCommand(
            command='help', description='Помощь'
        ),
        BotCommand(
            command='help_kb', description='Помощь с цифрыми'
        ),
        BotCommand(
            command='more', description='more'
        ),
        BotCommand(
            command='callback', description='callback'
        ),
     
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())





