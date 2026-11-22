from typing import Any
from dataclasses import dataclass
import string

@dataclass(eq=False, init=False)
class Aeroplane:
    __icao24: str
    __callsign: str | None
    __origin_country: str
    __baro_altitude: float | None
    __velocity: float | None
    __vertical_rate: float | None

    def __init__(
        self,
        icao24: str,
        callsign: str | None,
        origin_country: str,
        baro_altitude: float | None,
        velocity: float | None,
        vertical_rate: float | None,
    ) -> None:
        self.__icao24 = icao24
        self.__callsign = callsign
        self.__origin_country = origin_country
        self.__baro_altitude = baro_altitude
        self.__velocity = velocity
        self.__vertical_rate = vertical_rate

        self.__post_init__()

    # Публичный доступ к атрибутам

    @property
    def icao24(self) -> str:
        return self.__icao24

    @property
    def callsign(self) -> str | None:
        return self.__callsign

    @property
    def origin_country(self) -> str:
        return self.__origin_country

    @property
    def baro_altitude(self) -> float | None:
        return self.__baro_altitude

    @property
    def velocity(self) -> float | None:
        return self.__velocity

    @property
    def vertical_rate(self) -> float | None:
        return self.__vertical_rate

    @classmethod
    def cast_to_object_list(cls, opensky_response: dict[str, Any]) -> list["Aeroplane"]:
        states = opensky_response.get("states") or []
        aeroplanes: list[Aeroplane] = []


        for state in states:
            if not state[2] or not state[2].strip():
                continue
            raw_data = state[1]
            clean_data = raw_data.strip() if raw_data else None

            plane = cls(
                icao24 = state[0],
                callsign = clean_data,
                origin_country=state[2],
                baro_altitude=state[7],
                velocity=state[9],
                vertical_rate=state[11],
            )
            aeroplanes.append(plane)
        return aeroplanes

    def __lt__(self, other: object) -> bool:
        """Метод для сравнивания высоты полета"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self.baro_altitude is None or other.baro_altitude is None:
            raise ValueError("Невозможно сравнить, т.к. у одного из самолетов высота = None")
        return self.baro_altitude < other.baro_altitude

    def __gt__(self, other: object) -> bool:
        """Метод для сравнивания высоты полета"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self.baro_altitude is None or other.baro_altitude is None:
            raise ValueError("Невозможно сравнить, т.к. у одного из самолетов высота = None")
        return self.baro_altitude > other.baro_altitude

    def __eq__(self, other: object) -> bool:
        """Проверка идентичности самолётов по уникальному адресу icao24"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.icao24 == other.icao24

    def is_faster_than(self, other: "Aeroplane") -> bool:
        """Проверяет быстрее ли текущий самолёт чем переданный"""
        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно только с другим объектом Aeroplane")
        if self.velocity is None or other.velocity is None:
            raise ValueError("Невозможно сравнить, т.к. у одного из самолетов скорость = None")
        return self.velocity > other.velocity

    def __post_init__(self) -> None:
        """Валидация"""
        # Проверка ICAO24
        if not isinstance(self.icao24, str):
            raise TypeError("ICAO24 должен быть строкой")

        if len(self.icao24) != 6 or not all(
                char in string.hexdigits for char in self.icao24
        ):
            raise ValueError("ICAO24 должен содержать 6 шестнадцатеричных символов")

        # Проверка callsign
        if self.callsign is not None and not isinstance(self.callsign, str):
            raise TypeError("Callsign должен быть строкой или None")

        # Проверка страны
        if not isinstance(self.origin_country, str):
            raise TypeError("Страна должна быть строкой")

        if not self.origin_country.strip():
            raise ValueError("Страна не может быть пустой")

        # Проверка числовых значений
        numeric_fields = {
            "baro_altitude": self.baro_altitude,
            "velocity": self.velocity,
            "vertical_rate": self.vertical_rate,
        }

        for field_name, value in numeric_fields.items():
            if value is not None and (
                    isinstance(value, bool) or not isinstance(value, (int, float))
            ):
                raise TypeError(f"{field_name} должен быть числом или None")

        # Проверка неотрицательной скорости
        if self.velocity is not None and self.velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")



