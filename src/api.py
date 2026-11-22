from typing import Any

import requests
from src.base_api import BaseAPI
from src.aeroplane import Aeroplane


class NominatimAPI(BaseAPI):
    def __init__(self) -> None:

        base_url = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "test-app/1.0"}

        super().__init__(base_url, headers)

    def get_data(self, params: dict) -> list[dict[str, Any]]:
        """Получает данные о географическом положении"""
        response = requests.get(
            self.base_url, params=params, headers=self.headers, timeout=10
        )
        self.validate_response(response)
        return response.json()

    def validate_response(self, response: requests.Response) -> bool:
        """Проверяет корректномть HTTP запроса"""
        response.raise_for_status()
        return True


class OpenSkyAPI(BaseAPI):
    def __init__(self) -> None:
        base_url = "https://opensky-network.org/api/states/all"
        headers = {"User-Agent": "test-app/1.0"}
        super().__init__(base_url, headers)

    def get_data(self, params: dict) -> dict[str, Any]:
        response = requests.get(
            self.base_url, params=params, headers=self.headers, timeout=10
        )
        self.validate_response(response)
        return response.json()

    def validate_response(self, response: requests.Response) -> bool:
        response.raise_for_status()
        return True


class AeroplanesAPI:
    def __init__(self) -> None:
        self.nominatim = NominatimAPI()
        self.opensky = OpenSkyAPI()

    def get_aeroplanes(self, country: str) -> list[Aeroplane]:
        """Метод для получения данных о самолётах над страной"""
        nominatim_params = {"country": country, "format": "json", "limit": 1}
        geo_data = self.nominatim.get_data(nominatim_params)
        if not geo_data or not geo_data[0].get("boundingbox"):
            raise ValueError(f"No data found for {country}")

        bbox = geo_data[0]["boundingbox"]
        opensky_params = {
            "lamin": float(bbox[0]),
            "lamax": float(bbox[1]),
            "lomin": float(bbox[2]),
            "lomax": float(bbox[3]),
        }
        opensky_data = self.opensky.get_data(opensky_params)
        return Aeroplane.cast_to_object_list(opensky_data)
