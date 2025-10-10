from aiogram import Router, types
from aiogram.enums import ParseMode

from app.utils.escape import escape_markdown
from app.services.agent import get_agent

router = Router(name="mcp_handler")



@router.message(lambda x: x == x)
async def mcp_handler(message: types.Message) -> None:
    agent = await get_agent()
    config = {"configurable": {"session_id": str(message.chat.id)}}
    result = await agent.ainvoke({"input": message.text}, config)
    answer = escape_markdown(result["output"])
    await message.answer(answer, parse_mode=ParseMode.MARKDOWN_V2)