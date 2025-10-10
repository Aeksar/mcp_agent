from __future__ import print_function

import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import datetime
from datetime import date, datetime, timedelta, timezone
import pytz
from typing import List

from base import CalendarService, Event

class GoogleCalendarService(CalendarService):
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(self, credentials_file="credentials.json", token_file="token.json"):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        self.service = None
        self.events = {} # name: event_id
        self.timezone = pytz.timezone("Europe/Moscow")
        self._authenticate()

    def _authenticate(self):
        """Авторизация и создание клиента."""
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(self.token_file, "w") as token:
                token.write(self.creds.to_json())

        self.service = build("calendar", "v3", credentials=self.creds)

    # ---------- Вспомогательная функция ----------

    def _get_events_by_date(self, target_date: date) -> List[Event]:
        """Возвращает события за конкретный день."""
        start_of_day = datetime.combine(target_date, datetime.min.time(), tzinfo=self.timezone).isoformat()
        end_of_day = datetime.combine(target_date, datetime.max.time(), tzinfo=self.timezone).isoformat()

        events_result = self.service.events().list(
            calendarId="primary",
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])
        result = []

        for event in events:
            start_str = event["start"].get("dateTime", event["start"].get("date"))
            end_str = event["end"].get("dateTime", event["end"].get("date"))

            # Парсим ISO8601 в date
            start_date = datetime.fromisoformat(start_str)
            end_date = datetime.fromisoformat(end_str)

            result.append(Event(name=event.get("summary", "(Без названия)"),
                                start=start_date, end=end_date))
        return result

    # ---------- Методы интерфейса ----------

    def get_today_events(self) -> List[Event]:
        today = datetime.now(self.timezone)
        return self._get_events_by_date(today)

    def get_tomorrow_events(self) -> List[Event]:
        tomorrow = datetime.now(self.timezone) + timedelta(days=1)
        return self._get_events_by_date(tomorrow)


    def add_event(self, name: str, start: datetime, end: datetime) -> None:
        """Добавляет событие в календарь."""
        # Конвертируем даты в datetime UTC
        start = start - timedelta(hours=3)
        end = end - timedelta(hours=3)
        start_datetime = start.isoformat() + "Z"
        end_datetime = end.isoformat() + "Z"
        print(start_datetime, end_datetime)
        event_body = {
            "summary": name,
            "start": {
                "dateTime": start_datetime,
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": "UTC"
            },
        }

        event = self.service.events().insert(calendarId="primary", body=event_body).execute()
        self.events[name] = event.get("id")
        return {"message": "Событие добавлено"}

    def delete_event(self, event_id: str) -> None:
        """Удаляет событие по Названию."""
        try:
            # event_id = self.events.get(name)
            # if not event_id:
            #     return {"message": "Событие не найдено"}
            self.service.events().delete(calendarId="primary", eventId=event_id).execute()
            return {"message": "Событие удалено"}
        except Exception as e:
            return {"message": "Произошла ошибка при удалении события"}

if __name__ == '__main__':
    calendar_service = GoogleCalendarService()
    events = calendar_service.get_today_events()
    print(f"events: {events}")
