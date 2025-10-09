import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.configs.settings import settings

async def main() -> None:
    logging.info("Starting bot")
    if not settings.bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
    bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    from app.bots.router import router
    dp.include_router(router)
    logging.info("Bot started")
    await dp.start_polling(bot)
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

