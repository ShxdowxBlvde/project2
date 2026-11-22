import os
import json
from typing import Any

from src.base_saver import BaseSaver
from src.aeroplane import Aeroplane


class JSONSaver(BaseSaver):
    """Класс для сохранения, чтения и удаления данных о самолётах в JSON"""

    def __init__(self, filename: str = "aeroplanes.json") -> None:
        self.__filename = filename

    def _read_file(self) -> list[dict[str, Any]]:
        """Безопасное чтение данных из JSON"""

        if not os.path.exists(self.__filename):
            return []

        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []

        except (json.JSONDecodeError, OSError):
            return []

    def _write_file(self, data: list[dict[str, Any]]) -> None:
        """Запись списка словарей в JSON"""

        directory = os.path.dirname(self.__filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def _aeroplane_to_dict(plane: Aeroplane) -> dict[str, Any]:
        """Преобразует объект Aeroplane в словарь"""

        return {
            "icao24": plane.icao24,
            "callsign": plane.callsign,
            "origin_country": plane.origin_country,
            "baro_altitude": plane.baro_altitude,
            "velocity": plane.velocity,
            "vertical_rate": plane.vertical_rate,
        }

    def add_aeroplanes(self, aeroplanes: list[Aeroplane]) -> None:
        """Добавляет самолёты или обновляет существующие записи по ICAO24"""

        existing_data = self._read_file()

        # Индексируем существующие записи по уникальному ICAO24
        planes_by_icao = {
            item["icao24"]: item
            for item in existing_data
            if "icao24" in item
        }

        for plane in aeroplanes:
            planes_by_icao[plane.icao24] = self._aeroplane_to_dict(plane)

        self._write_file(list(planes_by_icao.values()))

    def get_aeroplanes(
        self, criteria: dict[str, Any] | None = None
    ) -> list[Aeroplane]:
        """Возвращает самолёты с учётом переданных критериев"""

        raw_data = self._read_file()
        result: list[Aeroplane] = []

        for item in raw_data:
            if criteria is not None:
                match = all(
                    item.get(key) == value
                    for key, value in criteria.items()
                )

                if not match:
                    continue

            result.append(Aeroplane(**item))

        return result

    def delete_aeroplanes(self, criteria: dict[str, Any]) -> None:
        """Удаляет самолёты по указанным критериям"""

        if not criteria:
            raise ValueError("Критерии удаления не могут быть пустыми")

        raw_data = self._read_file()

        filtered_data = [
            item
            for item in raw_data
            if not all(
                item.get(key) == value
                for key, value in criteria.items()
            )
        ]

        self._write_file(filtered_data)
