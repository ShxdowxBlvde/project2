import pytest

from src.aeroplane import Aeroplane
from src.saver import JSONSaver


@pytest.fixture
def json_saver(tmp_path):
    """Создаёт JSONSaver с временным файлом."""
    filename = tmp_path / "aeroplanes.json"
    return JSONSaver(str(filename))


@pytest.fixture
def aeroplane():
    """Создаёт тестовый объект самолёта."""
    return Aeroplane(
        icao24="3c675a",
        callsign="DLH123",
        origin_country="Germany",
        baro_altitude=10000.0,
        velocity=250.0,
        vertical_rate=0.0,
    )


@pytest.fixture
def another_aeroplane():
    """Создаёт второй тестовый объект самолёта."""
    return Aeroplane(
        icao24="4ca123",
        callsign="RYR456",
        origin_country="Ireland",
        baro_altitude=11000.0,
        velocity=230.0,
        vertical_rate=1.0,
    )


@pytest.fixture
def aeroplane_list(aeroplane, another_aeroplane):
    """Возвращает список тестовых самолётов."""
    return [aeroplane, another_aeroplane]


@pytest.fixture
def aeroplane_factory():
    """Создаёт самолёт с параметрами по умолчанию и позволяет их менять."""

    def factory(**kwargs):
        data = {
            "icao24": "3c675a",
            "callsign": "DLH123",
            "origin_country": "Germany",
            "baro_altitude": 10000.0,
            "velocity": 250.0,
            "vertical_rate": 0.0,
        }
        data.update(kwargs)
        return Aeroplane(**data)

    return factory
