import pytest

from src.aeroplane import Aeroplane
from src.saver import JSONSaver


def test_add_single_aeroplane(json_saver, aeroplane):
    """Проверяет добавление одного самолёта."""
    json_saver.add_aeroplanes([aeroplane])

    result = json_saver.get_aeroplanes()

    assert len(result) == 1
    assert result[0].icao24 == aeroplane.icao24


def test_add_multiple_aeroplanes(json_saver, aeroplane_list):
    """Проверяет добавление нескольких самолётов."""
    json_saver.add_aeroplanes(aeroplane_list)

    result = json_saver.get_aeroplanes()

    assert len(result) == 2


def test_update_existing_aeroplane(json_saver, aeroplane):
    """Проверяет обновление существующего самолёта по ICAO24."""
    json_saver.add_aeroplanes([aeroplane])

    updated_plane = Aeroplane(
        icao24="3c675a",
        callsign="DLH999",
        origin_country="Germany",
        baro_altitude=12000.0,
        velocity=300.0,
        vertical_rate=2.0,
    )

    json_saver.add_aeroplanes([updated_plane])

    result = json_saver.get_aeroplanes()

    assert len(result) == 1
    assert result[0].callsign == "DLH999"
    assert result[0].velocity == 300.0


def test_get_all_aeroplanes(json_saver, aeroplane_list):
    """Проверяет получение всех самолётов."""
    json_saver.add_aeroplanes(aeroplane_list)

    result = json_saver.get_aeroplanes()

    assert len(result) == 2
    assert all(isinstance(plane, Aeroplane) for plane in result)


def test_get_aeroplanes_by_criteria(json_saver, aeroplane_list):
    """Проверяет фильтрацию самолётов по стране."""
    json_saver.add_aeroplanes(aeroplane_list)

    result = json_saver.get_aeroplanes(
        criteria={"origin_country": "Germany"}
    )

    assert len(result) == 1
    assert result[0].origin_country == "Germany"


def test_delete_aeroplane(json_saver, aeroplane_list):
    """Проверяет удаление самолёта по ICAO24."""
    json_saver.add_aeroplanes(aeroplane_list)

    json_saver.delete_aeroplanes(
        criteria={"icao24": "3c675a"}
    )

    result = json_saver.get_aeroplanes()

    assert len(result) == 1
    assert result[0].icao24 == "4ca123"


def test_delete_nonexistent_aeroplane(json_saver, aeroplane_list):
    """Проверяет удаление по несуществующему критерию."""
    json_saver.add_aeroplanes(aeroplane_list)

    json_saver.delete_aeroplanes(
        criteria={"icao24": "ffffff"}
    )

    result = json_saver.get_aeroplanes()

    assert len(result) == 2


def test_delete_with_empty_criteria(json_saver, aeroplane):
    """Проверяет защиту от удаления с пустыми критериями."""
    json_saver.add_aeroplanes([aeroplane])

    with pytest.raises(ValueError):
        json_saver.delete_aeroplanes(criteria={})

    assert len(json_saver.get_aeroplanes()) == 1


def test_get_aeroplanes_from_empty_file(json_saver):
    """Проверяет получение данных из отсутствующего файла."""
    result = json_saver.get_aeroplanes()

    assert result == []
