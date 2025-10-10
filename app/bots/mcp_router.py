from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StreamableHttpConnection
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

from datetime import datetime

from app.configs.settings import settings
from app.utils.escape import escape_markdown

client = MultiServerMCPClient(
    {
        "calendar": StreamableHttpConnection(
                transport=settings.mcp_calendar.transport,
                url=settings.mcp_calendar.url,
                timeout=settings.mcp_calendar.mcp_request_timeout_sec
            )
    }
)
llm = ChatMistralAI(
    model="mistral-large-latest",
    mistral_api_key=settings.mistral_api_key,
)

tamplate = ChatPromptTemplate.from_messages([
    ("system", f"You are a helpful assistant.\n current_time: {datetime.now()}"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

router = Router(name="mcp_handler")

async def get_agent_executor():
    tools = await client.get_tools()
    print(tools)
    agent = create_tool_calling_agent(
        llm,
        tools,
        tamplate,
    )
    return AgentExecutor.from_agent_and_tools(agent, tools)


@router.message(lambda x: x == x)
async def mcp_handler(message: types.Message) -> None:
    agent = await get_agent_executor()
    result = await agent.ainvoke({"input": message.text})
    answer = escape_markdown(result["output"])
    await message.answer(answer, parse_mode=ParseMode.MARKDOWN_V2)