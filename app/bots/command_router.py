from aiogram import Router, types
from aiogram.filters import Command


router = Router(name="commands")



@router.message(Command("health"))
async def health(message: types.Message) -> None:
    await message.answer("ok")


@router.message(Command("help"))
async def help_cmd(message: types.Message) -> None:
    text = (
        "Commands:\n"
        "/health - check status\n"
        "/help - show this help\n"
        "/today - show today calendar (MCP stub)"
    )
    await message.answer(text)
