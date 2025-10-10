from __future__ import annotations

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import StdioConnection, StreamableHttpConnection
from typing import Any, Dict, Optional

from configs.settings import MCPSettings



class CalendarMcpClient():
    def __init__(
        self,
        calendar_settings: MCPSettings,
    ) -> None:
        self.client = None
        if calendar_settings.url:
            self.client = MultiServerMCPClient(
                connections=StreamableHttpConnection(
                    transport=calendar_settings.transport,
                    url=calendar_settings.url,
                    timeout=calendar_settings.mcp_request_timeout_sec,
                    )
                )
        elif calendar_settings.command and calendar_settings.args:
            self.client = MultiServerMCPClient(
                connections=StdioConnection(
                    transport=calendar_settings.transport,
                    command=calendar_settings.command,
                    args=[calendar_settings.args],
                    timeout=calendar_settings.mcp_request_timeout_sec,
                    )
                )
        else:
            raise ValueError("MCP_CALENDAR_URL or (MCP_CALENDAR_CMD and MCP_CALENDAR_ARGS) must be set")
        
        
