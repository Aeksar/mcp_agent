from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StreamableHttpConnection
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.tools import Tool

from app.vectordb.store import get_store
from app.configs.settings import settings


from app.configs.settings import settings


def get_mcp_client():
    client = MultiServerMCPClient(
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

    return client

def rag_search(query: str) -> str:
    store = get_store(settings.collection_name)
    retriever = store.as_retriever(k=5)
    docs = retriever.invoke(query)
    return "\n\n".join([d.page_content for d in docs])


async def get_tools():
    rag_tool = Tool(
        name="knowledge_base_search",
        func=rag_search,
        description="Useful for searching internal knowledge base for reports and documentation."
    )

    mcp_client = get_mcp_client()
    mcp_tools = await mcp_client.get_tools()
    mcp_tools.append(rag_tool)
    return mcp_tools