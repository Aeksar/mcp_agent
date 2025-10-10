from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from datetime import datetime



class Event(BaseModel):
    name: str = Field(str, description="Название события")
    start: datetime = Field(datetime, description="Дата начала события")
    end: datetime = Field(datetime, description="Дата окончания события")


class CalendarService(ABC):
    @abstractmethod
    def get_today_events(self) -> list[Event]: ...

    @abstractmethod
    def get_tomorrow_events(self):...

    @abstractmethod
    def add_event(self, name: str, start: datetime, end: datetime): ...