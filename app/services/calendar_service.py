from __future__ import annotations

from typing import Any, List

from app.mcp.calendar import CalendarMcpClient
from app.configs.settings import settings


class CalendarService:
    def __init__(self) -> None:
        self.client = CalendarMcpClient(
            server_command=settings.mcp_calendar_cmd,
            host=settings.mcp_calendar_host,
            port=settings.mcp_calendar_port,
            request_timeout_sec=settings.mcp_request_timeout_sec,
        )

    async def list_today(self) -> List[dict[str, Any]]:
        response = await self.client.call("list_today_events")
        if not response.ok:
            return []
        assert isinstance(response.data, list)
        return response.data


