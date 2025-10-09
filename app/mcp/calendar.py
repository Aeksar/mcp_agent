from __future__ import annotations

from typing import Any, Dict, Optional

from .base import McpClient, McpResponse, McpError


class CalendarMcpClient(McpClient):
    def __init__(
        self,
        server_command: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        request_timeout_sec: int = 30,
    ) -> None:
        super().__init__(server_command, host, port, request_timeout_sec)
        self._transport = None
        self._session = None

    async def start(self) -> None:
        if self._session is not None:
            return
        if not self.server_command:
            raise McpError("MCP_CALENDAR_CMD is not configured")
        try:
            # Lazy import to avoid hard dependency if not used elsewhere
            from mcp.client.session import ClientSession  # type: ignore
            from mcp.transport.stdio import StdioTransport  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise McpError(f"Failed to import mcp library: {exc}")

        # Spawn the MCP server process and establish stdio transport
        self._transport = await StdioTransport.create(self.server_command)
        self._session = ClientSession(self._transport)
        await self._session.initialize()

    async def stop(self) -> None:
        if self._session is not None:
            try:
                await self._session.close()
            finally:
                self._session = None
        if self._transport is not None:
            try:
                await self._transport.close()
            finally:
                self._transport = None

    async def call(self, tool: str, arguments: Dict[str, Any] | None = None) -> McpResponse:
        if self._session is None:
            await self.start()
        assert self._session is not None
        try:
            result = await self._session.call_tool(tool, arguments or {})
            # Expecting result in JSON-serializable form from MCP server
            return McpResponse(ok=True, data=result)
        except Exception as exc:
            return McpResponse(ok=False, error=str(exc))


