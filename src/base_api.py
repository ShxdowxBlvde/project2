from abc import ABC, abstractmethod
from typing import Any


class BaseAPI(ABC):
    def __init__(self, base_url: str, headers: dict) -> None:
        self.base_url = base_url
        self.headers = headers

    @abstractmethod
    def get_data(self, params: dict) -> Any:
        """Получение данных от API"""
        pass

    @abstractmethod
    def validate_response(self, response) -> bool:
        """Проверка ответа API"""
        pass
