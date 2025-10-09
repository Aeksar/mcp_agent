#!/usr/bin/env python3
"""
Custom MCP server for Google Calendar using standard MCP protocol
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}", file=sys.stderr)
    print("Continuing without .env file...", file=sys.stderr)

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Initialize MCP server
server = Server("google-calendar")

# Global service instance
service = None


def get_credentials() -> Optional[Credentials]:
    """Get valid user credentials from storage or prompt for authorization."""
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use environment variables for OAuth credentials
            client_id = os.getenv('GOOGLE_CLIENT_ID')
            client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
            redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:3000/auth/callback')
            
            if not all([client_id, client_secret]):
                print("Error: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in environment", file=sys.stderr)
                print("Please create a .env file with your Google OAuth credentials or set environment variables", file=sys.stderr)
                return None
            
            # Create OAuth flow
            flow = InstalledAppFlow.from_client_config(
                {
                    "installed": {
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [redirect_uri]
                    }
                },
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds


def get_calendar_service():
    """Get Google Calendar service instance."""
    global service
    if service is None:
        creds = get_credentials()
        if creds:
            service = build('calendar', 'v3', credentials=creds)
    return service


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="list_today_events",
            description="List all events for today",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="list_week_events", 
            description="List all events for the current week",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="create_event",
            description="Create a new calendar event",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Event title"},
                    "start_time": {"type": "string", "description": "Start time in ISO format"},
                    "end_time": {"type": "string", "description": "End time in ISO format"},
                    "description": {"type": "string", "description": "Event description"},
                    "location": {"type": "string", "description": "Event location"}
                },
                "required": ["title", "start_time", "end_time"]
            }
        ),
        Tool(
            name="search_events",
            description="Search for events by query string",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer", "description": "Maximum number of results", "default": 10}
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    try:
        service = get_calendar_service()
        if not service:
            return [TextContent(type="text", text=json.dumps({"error": "Failed to initialize Google Calendar service"}))]
        
        if name == "list_today_events":
            result = await list_today_events(service)
        elif name == "list_week_events":
            result = await list_week_events(service)
        elif name == "create_event":
            result = await create_event(service, **arguments)
        elif name == "search_events":
            result = await search_events(service, **arguments)
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result))]
        
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def list_today_events(service) -> Dict[str, Any]:
    """List all events for today."""
    # Get today's date range
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    # Format for Google Calendar API
    time_min = start_of_day.isoformat() + 'Z'
    time_max = end_of_day.isoformat() + 'Z'
    
    # Call the Calendar API
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    # Format events for response
    formatted_events = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        formatted_events.append({
            'title': event.get('summary', 'No Title'),
            'start': start,
            'end': end,
            'description': event.get('description', ''),
            'location': event.get('location', ''),
            'status': event.get('status', '')
        })
    
    return {
        "success": True,
        "events": formatted_events,
        "count": len(formatted_events)
    }


async def list_week_events(service) -> Dict[str, Any]:
    """List all events for the current week."""
    # Get current week's date range
    now = datetime.utcnow()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=7)
    
    # Format for Google Calendar API
    time_min = start_of_week.isoformat() + 'Z'
    time_max = end_of_week.isoformat() + 'Z'
    
    # Call the Calendar API
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    # Format events for response
    formatted_events = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        formatted_events.append({
            'title': event.get('summary', 'No Title'),
            'start': start,
            'end': end,
            'description': event.get('description', ''),
            'location': event.get('location', ''),
            'status': event.get('status', '')
        })
    
    return {
        "success": True,
        "events": formatted_events,
        "count": len(formatted_events)
    }


async def create_event(service, title: str, start_time: str, end_time: str, description: str = "", location: str = "") -> Dict[str, Any]:
    """Create a new calendar event."""
    # Create event body
    event_body = {
        'summary': title,
        'description': description,
        'location': location,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
    }
    
    # Create the event
    created_event = service.events().insert(
        calendarId='primary',
        body=event_body
    ).execute()
    
    return {
        "success": True,
        "event_id": created_event.get('id'),
        "event_link": created_event.get('htmlLink'),
        "message": f"Event '{title}' created successfully"
    }


async def search_events(service, query: str, max_results: int = 10) -> Dict[str, Any]:
    """Search for events by query string."""
    # Search for events
    events_result = service.events().list(
        calendarId='primary',
        q=query,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    # Format events for response
    formatted_events = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        
        formatted_events.append({
            'title': event.get('summary', 'No Title'),
            'start': start,
            'end': end,
            'description': event.get('description', ''),
            'location': event.get('location', ''),
            'status': event.get('status', '')
        })
    
    return {
        "success": True,
        "events": formatted_events,
        "count": len(formatted_events),
        "query": query
    }


async def main():
    """Run the MCP server."""
    print("Starting Google Calendar MCP Server...", file=sys.stderr)
    print("Available tools:", file=sys.stderr)
    print("- list_today_events: List today's events", file=sys.stderr)
    print("- list_week_events: List this week's events", file=sys.stderr) 
    print("- create_event: Create a new event", file=sys.stderr)
    print("- search_events: Search for events", file=sys.stderr)
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())