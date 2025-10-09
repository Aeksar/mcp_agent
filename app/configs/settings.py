from dataclasses import dataclass
import os
import dotenv

dotenv.load_dotenv()

@dataclass
class Settings:
    bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN")
    environment: str = os.getenv("ENV", "dev")
    # MCP: Google Calendar server configuration
    mcp_calendar_cmd: str | None = os.getenv("MCP_CALENDAR_CMD")
    mcp_calendar_host: str | None = os.getenv("MCP_CALENDAR_HOST", "localhost")
    mcp_calendar_port: int | None = (
        int(os.getenv("MCP_CALENDAR_PORT", "3000")) if os.getenv("MCP_CALENDAR_PORT") else None
    )
    mcp_request_timeout_sec: int = int(os.getenv("MCP_REQUEST_TIMEOUT_SEC", "30"))

settings = Settings()
