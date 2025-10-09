import asyncio
from aiogram import Bot
from aiogram.types import BotCommand
from app.configs.settings import settings


async def main() -> None:
    bot = Bot(settings.bot_token)
    commands = [
        BotCommand(command="help", description="Help"),
        BotCommand(command="health", description="Healthcheck"),
    ]
    await bot.set_my_commands(commands)


if __name__ == "__main__":
    asyncio.run(main())
