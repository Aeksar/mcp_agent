from aiogram import Router, types
from aiogram.filters import Command

router = Router(name= root)

@router.message(Command(health))
async def health(message: types.Message) -> None:
    await message.answer(ok)

@router.message(Command(help))
async def help_cmd(message: types.Message) -> None:
    text = (
        Commands:\n
        /health - check status\n
        /help - show this help
    )
    await message.answer(text)
