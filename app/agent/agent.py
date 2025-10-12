from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_tool_calling_agent, AgentExecutor, initialize_agent, AgentType
from langchain_core.runnables.history import RunnableWithMessageHistory

from datetime import datetime

from app.configs.settings import settings
from app.memory.redis_memory import get_redis_memory

from .tools import get_tools
from .prompt import tamplate


llm = ChatMistralAI(
    model=settings.llm_model,
    mistral_api_key=settings.mistral_api_key,
)



async def get_agent():
    tools = await get_tools()
    print(tools)
    agent = create_tool_calling_agent(llm, tools, tamplate)
    agent_exec = AgentExecutor.from_agent_and_tools(agent, tools)
    agent_with_history = RunnableWithMessageHistory(
        agent_exec,
        get_redis_memory,
        input_messages_key="input",
        history_messages_key="history",
        output_messages_key="output"
    )
    return agent_with_history
