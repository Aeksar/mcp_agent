from aiogram import Router, types
from aiogram.enums import ParseMode
from httpx import HTTPStatusError

from app.utils.escape import escape_markdown
from app.agent.agent import get_agent

router = Router(name="mcp_handler")



@router.message(lambda x: x == x)
async def mcp_handler(message: types.Message) -> None:
    try:
        agent = await get_agent()
        config = {"configurable": {"session_id": str(message.chat.id)}}
        result = await agent.ainvoke({"input": message.text}, config)
        answer = escape_markdown(result["output"])
        await message.answer(answer, parse_mode=ParseMode.MARKDOWN_V2)
    except HTTPStatusError as e:
        await message.answer("Модель перегружена\nОтправте свое сообщение позже")