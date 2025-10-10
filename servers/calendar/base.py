from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from datetime import date



class Event(BaseModel):
    name: str = Field(str, description="Название события")
    start: date = Field(date, description="Дата начала события")
    end: date = Field(date, description="Дата окончания события")


class CalendarService(ABC):
    @abstractmethod
    def get_today_events(self) -> list[Event]:
        """
        Возвращает события на сегодня из основного календаря.
        :return: Список событий на сегодня в формате словаря, где каждый словарь содержит
            поля "start" (дата начала события), "end" (дата конца события) и "name" (название события)
        :rtype: List[Dict[str, date | str]]
        """
        pass

    @abstractmethod
    def get_tomorrow_events(self):
        """
        Возвращает события на завтра из основного календаря.
        :return: Список событий на завтра в формате словаря, где каждый словарь содержит
            поля "start" (дата начала события), "end" (дата конца события) и "name" (название события)
        :rtype: List[Dict[str, date | str]]
        """
        pass

    @abstractmethod
    def add_event(self, name: str, start: date, end: date):
        """
        Добавляет событие в основной календарь.
        :param name: Название события
        :param start: Дата начала события
        :param end: Дата окончания события
        :return: None
        :rtype: None
        """
        pass

    def delete_event(self):
        """
        Удаляет событие из основного календаря.
        :param event_id: Идентификатор события
        :return: None
        :rtype: None
        """
        pass