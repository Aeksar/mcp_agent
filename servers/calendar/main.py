from mcp.server.fastmcp import FastMCP
from service import GoogleCalendarService

from datetime import datetime

mcp = FastMCP("calendar")
calendar_service = GoogleCalendarService()


@mcp.tool()
def get_today_events():
    """
    Get the events happening today.

    Returns:
        dict: A dictionary containing the events for today. The dictionary has a key "events" with the retrieved events as its value.
    """
    events = calendar_service.get_today_events()
    return {"events": events}


@mcp.tool()
def get_tomorrow_events():
    
    """
    Returns a list of events for tomorrow from the main calendar.

    :return: A dictionary containing a list of events for tomorrow
    :rtype: Dict[str, List[Dict[str, date | str]]]
    """
    events = calendar_service.get_tomorrow_events()
    return {"events": events}

@mcp.tool()
def add_event(name: str, start: datetime, end: datetime):
    
    """
    Adds an event to the main calendar.

    :param name: The name of the event
    :param start: The start date of the event in ISO 8601 format
    :param end: The end date of the event in ISO 8601 format
    :return: A dictionary containing a message indicating the event was added
    :rtype: Dict[str, str]
    """
    print(name, start, end)
    calendar_service.add_event(name, start, end)

    return {"message": "Event added"}

@mcp.tool()
def delete_event(event_id: str):
    """
    Deletes an event from the main calendar.

    :param event_id: The ID of the event to delete
    :return: A dictionary containing a message indicating the event was deleted
    :rtype: Dict[str, str]
    """
    calendar_service = GoogleCalendarService()
    calendar_service.delete_event(event_id)
    return {"message": "Event deleted"}


if __name__ == '__main__':
    # from datetime import timedelta
    # res = calendar_service.add_event("test", datetime.now(), datetime.now() + timedelta(days=1))
    # print(res)
    mcp.run(transport="streamable-http")