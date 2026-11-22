from abc import ABC, abstractmethod
from typing import Any
from src.aeroplane import Aeroplane


class BaseSaver(ABC):
    """Абстрактный класс для работы с файлами о самолетах"""
    @abstractmethod
    def add_aeroplanes(self, aeroplanes: list[Aeroplane]) -> None:
        """Добавляет информацию о самолетах в файл"""
        pass

    @abstractmethod
    def get_aeroplanes(self, criteria: dict[str, Any] | None = None) -> list[Aeroplane]:
        """Получает информацию по определенным критериям"""
        pass

    @abstractmethod
    def delete_aeroplanes(self, criteria: dict[str, Any]) -> None:
        """Удаляет информацию о самолете по указанным критериям"""
        pass