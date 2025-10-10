import asyncio
from aiogram import Bot
from aiogram.types import BotCommand
from app.configs.settings import settings


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="help", description="Help"),
        BotCommand(command="health", description="Healthcheck"),
    ]
    await bot.set_my_commands(commands)
