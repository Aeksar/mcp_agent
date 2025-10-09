from dataclasses import dataclass
import os
import dotenv
import shlex

dotenv.load_dotenv()

@dataclass
class Settings:
    bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN")
    environment: str = os.getenv("ENV", "dev")
    # MCP: Google Calendar server configuration
    mcp_calendar_ws_url: str | None = os.getenv("MCP_CALENDAR_WS_URL")
    mcp_calendar_cmd: str | None = os.getenv("MCP_CALENDAR_CMD")
    mcp_calendar_args: list[str] | None = None
    mcp_calendar_host: str | None = os.getenv("MCP_CALENDAR_HOST", "localhost")
    mcp_calendar_port: int | None = (
        int(os.getenv("MCP_CALENDAR_PORT", "3000")) if os.getenv("MCP_CALENDAR_PORT") else None
    )
    mcp_request_timeout_sec: int = int(os.getenv("MCP_REQUEST_TIMEOUT_SEC", "30"))
    # Google Calendar OAuth credentials for MCP server
    google_client_id: str | None = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret: str | None = os.getenv("GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str | None = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/callback")
    google_refresh_token: str | None = os.getenv("GOOGLE_REFRESH_TOKEN")

settings = Settings()
_args_raw = os.getenv("MCP_CALENDAR_ARGS")
if _args_raw:
    try:
        settings.mcp_calendar_args = shlex.split(_args_raw)
    except Exception:
        settings.mcp_calendar_args = _args_raw.split()
