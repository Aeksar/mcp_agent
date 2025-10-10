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
class GoogleOAuthCredentials:
    google_client_id: str | None = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret: str | None = os.getenv("GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str | None = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/callback")
    google_refresh_token: str | None = os.getenv("GOOGLE_REFRESH_TOKEN")


@dataclass
class Settings:
    bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN")
    mistral_api_key: str = os.getenv("MISTRAL_API_KEY")
    environment: str = os.getenv("ENV", "dev")
    mcp_calendar = MCPSettings("calendar")


settings = Settings()

if not settings.mcp_calendar.url and not (settings.mcp_calendar.command and settings.mcp_calendar.args):
    print(settings.mcp_calendar.url)
    raise ValueError("MCP_CALENDAR_URL or (MCP_CALENDAR_CMD and MCP_CALENDAR_ARGS) must be set")
