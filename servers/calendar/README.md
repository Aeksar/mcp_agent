# Google Calendar MCP Server

Custom MCP server for Google Calendar integration using `langchain-mcp-adapters` and `mcp.server.fastmcp`.

## Features

- List today's events
- List week's events  
- Create new events
- Search events by query

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up Google Calendar API credentials:
   - Copy `env_example.txt` to `.env`
   - Fill in your Google OAuth credentials:
     - `GOOGLE_CLIENT_ID`
     - `GOOGLE_CLIENT_SECRET`
     - `GOOGLE_REDIRECT_URI` (optional, defaults to http://localhost:3000/auth/callback)

3. Run the server:
   ```bash
   python calendar_server.py
   ```

## First Run

On first run, the server will:
1. Open a browser window for Google OAuth authorization
2. Save the refresh token to `token.json` for future use
3. Start the MCP server

## Available Tools

- `list_today_events()` - Get all events for today
- `list_week_events()` - Get all events for the current week
- `create_event(title, start_time, end_time, description?, location?)` - Create a new event
- `search_events(query, max_results?)` - Search for events by text

## Usage with MCP Agent

Update your agent's `.env`:
```env
MCP_CALENDAR_CMD=python
MCP_CALENDAR_ARGS=C:\\Users\\admin\\projects\\mcp_agent\\servers\\calendar\\calendar_server.py
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/callback
```

