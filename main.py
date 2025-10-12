import asyncio
import logging
from aiogram import Bot, Dispatcher

from app.configs.settings import settings
from app.bots import command_router, mcp_router


async def main() -> None:
    logging.info("Starting bot")
    if not settings.bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
    bot = Bot(settings.bot_token)
    dp = Dispatcher()
    dp.include_router(command_router)
    dp.include_router(mcp_router)
    logging.info("Bot started")
    await dp.start_polling(bot)
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

