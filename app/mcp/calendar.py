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
        self._client_cm = None  # async context manager for stdio_client
        self._session = None

    async def start(self) -> None:
        if self._session is not None:
            return
        from app.configs.settings import settings
        if not settings.mcp_calendar_ws_url and not self.server_command:
            raise McpError("Neither MCP_CALENDAR_WS_URL nor MCP_CALENDAR_CMD is configured")
        try:
            # Lazy import to avoid hard dependency if not used elsewhere
            from mcp.client.session import ClientSession  # type: ignore
            from mcp.client.stdio import StdioServerParameters, stdio_client  # type: ignore
            from mcp.client.websocket import websocket_client  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise McpError(f"Failed to import mcp library: {exc}")

        # Choose transport: WebSocket (docker service) > stdio fallback
        if settings.mcp_calendar_ws_url:
            self._client_cm = websocket_client(settings.mcp_calendar_ws_url)
            read_stream, write_stream = await self._client_cm.__aenter__()
            self._session = ClientSession(read_stream, write_stream)
            await self._session.initialize()
            return

        # Fallback to stdio with Google Calendar OAuth env vars
        args: list[str] = settings.mcp_calendar_args or []
        env_vars = {}
        if settings.google_client_id:
            env_vars["GOOGLE_CLIENT_ID"] = settings.google_client_id
        if settings.google_client_secret:
            env_vars["GOOGLE_CLIENT_SECRET"] = settings.google_client_secret
        if settings.google_redirect_uri:
            env_vars["GOOGLE_REDIRECT_URI"] = settings.google_redirect_uri
        if settings.google_refresh_token:
            env_vars["GOOGLE_REFRESH_TOKEN"] = settings.google_refresh_token
        
        self._client_cm = stdio_client(
            StdioServerParameters(command=self.server_command, args=args, env=env_vars)
        )
        read_stream, write_stream = await self._client_cm.__aenter__()
        self._session = ClientSession(read_stream, write_stream)
        await self._session.initialize()

    async def stop(self) -> None:
        if self._session is not None:
            self._session = None
        if self._client_cm is not None:
            try:
                await self._client_cm.__aexit__(None, None, None)
            finally:
                self._client_cm = None

    async def call(self, tool: str, arguments: Dict[str, Any] | None = None) -> McpResponse:
        if self._session is None:
            await self.start()
        assert self._session is not None
        try:
            print(f"calling tool: {tool} with arguments: {arguments}")
            result = await self._session.call_tool(tool, arguments or {})
            # Convert pydantic model to dict for downstream usage
            data = result.model_dump() if hasattr(result, "model_dump") else result
            return McpResponse(ok=True, data=data)
        except Exception as exc:
            return McpResponse(ok=False, error=str(exc))


