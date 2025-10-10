from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StreamableHttpConnection
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory

from datetime import datetime

from app.configs.settings import settings
from app.utils.escape import escape_markdown
from app.memory.redis_memory import get_redis_memory

mcp_client = MultiServerMCPClient(
    {
        "calendar": StreamableHttpConnection(
                transport=settings.mcp_calendar.transport,
                url=settings.mcp_calendar.url,
                timeout=settings.mcp_calendar.mcp_request_timeout_sec
            ),
        "mail": StreamableHttpConnection(
                transport=settings.mcp_mail.transport,
                url=settings.mcp_mail.url,
                timeout=settings.mcp_mail.mcp_request_timeout_sec
            ),
        "sheet": StreamableHttpConnection(
                transport=settings.mcp_sheet.transport,
                url=settings.mcp_sheet.url,
                timeout=settings.mcp_sheet.mcp_request_timeout_sec
            ),
        
    }
)
llm = ChatMistralAI(
    model="mistral-large-latest",
    mistral_api_key=settings.mistral_api_key,
)

tamplate = ChatPromptTemplate.from_messages([
    ("system", f"You are a helpful assistant.\n current_time: {datetime.now()}"),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

async def get_agent():
    tools = await mcp_client.get_tools()
    agent = create_tool_calling_agent(
        llm,
        tools,
        tamplate,
    )
    agent_exec = AgentExecutor.from_agent_and_tools(agent, tools)
    agent_with_history = RunnableWithMessageHistory(
        agent_exec,
        get_redis_memory,
        input_messages_key="input",
        history_messages_key="history",
        output_messages_key="output"
    )
    return agent_with_history
