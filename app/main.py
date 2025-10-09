import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from app.configs.settings import settings

async def main() -> None:
    if not settings.bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
    bot = Bot(settings.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    from app.bots.router import router
    dp.include_router(router)
    await dp.start_polling(bot)
        

if __name__ == "__main__":
    asyncio.run(main())

