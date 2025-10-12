from dataclasses import dataclass
import os
import dotenv
import shlex

dotenv.load_dotenv()

class MCPSettings:
    def __init__(self, service_name: str):
        self.transport: str = os.getenv(f"MCP_{service_name.upper()}_TRANSPORT", "streamable_http")
        self.url: str | None = os.getenv(f"MCP_{service_name.upper()}_URL")
        self.command: str | None = os.getenv(f"MCP_{service_name.upper()}_CMD")
        self.args: str | None = os.getenv(f"MCP_{service_name.upper()}_ARGS")
        self.mcp_request_timeout_sec: int = int(os.getenv("MCP_REQUEST_TIMEOUT_SEC", "30"))

@dataclass
class Settings:
    bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN")
    mistral_api_key: str = os.getenv("MISTRAL_API_KEY")

    mcp_calendar = MCPSettings("calendar")
    mcp_mail = MCPSettings("mail")
    mcp_sheet = MCPSettings("sheet")

    redis_url: str = os.getenv("REDIS_URL")
    qdrant_url: str = os.getenv("QDRANT_URL")

    embeddings_model: str = os.getenv("EMBEDDINGS_MODEL", "intfloat/multilingual-e5-base")
    llm_model: str = os.getenv("LLM_MODEL", "mistral-large-latest")
    collection_name: str = os.getenv("COLLECTION_NAME", "rag")

settings = Settings()
