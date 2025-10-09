from aiogram import Router, types
from aiogram.filters import Command

from app.services.calendar_service import CalendarService

router = Router(name="root")
calendar_service = CalendarService()


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


@router.message(Command("today"))
async def today_cmd(message: types.Message) -> None:
    events = await calendar_service.list_today()
    if not events:
        await message.answer("No events today.")
        return
    lines = ["Today:"]
    for e in events:
        title = str(e.get("title", "(no title)"))
        start = str(e.get("start", ""))
        end = str(e.get("end", ""))
        lines.append(f"- {start}-{end} {title}")
    await message.answer("\n".join(lines))
