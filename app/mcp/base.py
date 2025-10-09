from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


class McpError(Exception):
    pass


@dataclass
class McpResponse:
    ok: bool
    data: Any | None = None
    error: str | None = None


class McpClient:
    def __init__(
        self,
        server_command: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        request_timeout_sec: int = 30,
    ) -> None:
        self.server_command = server_command
        self.host = host
        self.port = port
        self.request_timeout_sec = request_timeout_sec

    async def start(self) -> None:
        """Start/connect to MCP server. Implement in subclasses."""
        raise NotImplementedError

    async def stop(self) -> None:
        """Stop/disconnect MCP server. Implement in subclasses."""
        raise NotImplementedError

    async def call(self, tool: str, arguments: Dict[str, Any] | None = None) -> McpResponse:
        """Call a tool on the MCP server.

        Subclasses must implement this using selected transport (process/stdio, TCP, etc.).
        """
        raise NotImplementedError


