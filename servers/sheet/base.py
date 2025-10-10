from abc import ABC, abstractmethod


class SheetService(ABC):
    @abstractmethod
    def get_data(self): ...

    @abstractmethod
    def set_data(self, data): ...

    @abstractmethod
    def append_data(self, data): ...

    @abstractmethod
    def clear_data(self): ...