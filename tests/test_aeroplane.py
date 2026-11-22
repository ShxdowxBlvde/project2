import pytest

from src.aeroplane import Aeroplane


def test_create_aeroplane(aeroplane):
    assert aeroplane.icao24 == "3c675a"
    assert aeroplane.callsign == "DLH123"
    assert aeroplane.origin_country == "Germany"
    assert aeroplane.baro_altitude == 10000.0
    assert aeroplane.velocity == 250.0
    assert aeroplane.vertical_rate == 0.0


# Проверка ICAO24

def test_invalid_icao24_type(aeroplane_factory):
    with pytest.raises(TypeError):
        aeroplane_factory(icao24=123456)


@pytest.mark.parametrize(
    "icao24",
    ["12345", "1234567", "ghijkl", "12345!"],
)
def test_invalid_icao24_value(aeroplane_factory, icao24):
    with pytest.raises(ValueError):
        aeroplane_factory(icao24=icao24)


# Проверка callsign

def test_invalid_callsign_type(aeroplane_factory):
    with pytest.raises(TypeError):
        aeroplane_factory(callsign=123)


def test_none_callsign(aeroplane_factory):
    plane = aeroplane_factory(callsign=None)
    assert plane.callsign is None


# Проверка страны

def test_invalid_country_type(aeroplane_factory):
    with pytest.raises(TypeError):
        aeroplane_factory(origin_country=123)


def test_empty_country(aeroplane_factory):
    with pytest.raises(ValueError):
        aeroplane_factory(origin_country="   ")


# Проверка числовых значений

@pytest.mark.parametrize(
    "field",
    ["baro_altitude", "velocity", "vertical_rate"],
)
def test_invalid_numeric_type(aeroplane_factory, field):
    with pytest.raises(TypeError):
        aeroplane_factory(**{field: "invalid"})


@pytest.mark.parametrize(
    "field",
    ["baro_altitude", "velocity", "vertical_rate"],
)
def test_boolean_is_not_valid_number(aeroplane_factory, field):
    with pytest.raises(TypeError):
        aeroplane_factory(**{field: True})


def test_negative_velocity(aeroplane_factory):
    with pytest.raises(ValueError):
        aeroplane_factory(velocity=-10)



def test_none_numeric_values(aeroplane_factory):
    plane = aeroplane_factory(
        baro_altitude=None,
        velocity=None,
        vertical_rate=None,
    )

    assert plane.baro_altitude is None
    assert plane.velocity is None
    assert plane.vertical_rate is None


# Проверка инкапсуляции

def test_properties_are_read_only(aeroplane):
    with pytest.raises(AttributeError):
        aeroplane.velocity = 300


# Проверка сравнения высоты

def test_compare_less_than(aeroplane, another_aeroplane):
    assert aeroplane < another_aeroplane


def test_compare_greater_than(aeroplane, another_aeroplane):
    assert another_aeroplane > aeroplane


def test_compare_altitude_with_none(aeroplane, aeroplane_factory):
    plane = aeroplane_factory(baro_altitude=None)

    with pytest.raises(ValueError):
        aeroplane < plane


def test_compare_with_other_type(aeroplane):
    with pytest.raises(TypeError):
        aeroplane < 100


# Проверка идентичности самолётов

def test_equal_aeroplanes(aeroplane, aeroplane_factory):
    another = aeroplane_factory(callsign="OTHER")

    assert aeroplane == another


def test_not_equal_aeroplanes(aeroplane, another_aeroplane):
    assert aeroplane != another_aeroplane


# Проверка сравнения скорости

def test_is_faster_than(aeroplane, another_aeroplane):
    assert aeroplane.is_faster_than(another_aeroplane)


def test_is_not_faster_than(aeroplane, another_aeroplane):
    assert not another_aeroplane.is_faster_than(aeroplane)


def test_is_faster_with_none_velocity(aeroplane, aeroplane_factory):
    plane = aeroplane_factory(velocity=None)

    with pytest.raises(ValueError):
        aeroplane.is_faster_than(plane)


def test_is_faster_with_invalid_object(aeroplane):
    with pytest.raises(TypeError):
        aeroplane.is_faster_than("plane")


# Проверка преобразования OpenSky

def test_cast_to_object_list():
    response = {
        "states": [
            [
                "3c675a", " DLH123 ", "Germany",
                None, None, None, None,
                10000.0, None, 250.0, None, 0.0
            ]
        ]
    }

    result = Aeroplane.cast_to_object_list(response)

    assert len(result) == 1
    assert isinstance(result[0], Aeroplane)
    assert result[0].icao24 == "3c675a"
    assert result[0].callsign == "DLH123"
    assert result[0].origin_country == "Germany"


def test_cast_to_object_list_skips_empty_country():
    response = {
        "states": [
            [
                "3c675a", "DLH123", "",
                None, None, None, None,
                10000.0, None, 250.0, None, 0.0
            ]
        ]
    }

    result = Aeroplane.cast_to_object_list(response)

    assert result == []


def test_cast_to_object_list_with_none_states():
    response = {"states": None}

    result = Aeroplane.cast_to_object_list(response)

    assert result == []


def test_cast_to_object_list_with_empty_response():
    result = Aeroplane.cast_to_object_list({})

    assert result == []

def test_negative_altitude_is_allowed(aeroplane_factory):
    plane = aeroplane_factory(baro_altitude=-100.0)

    assert plane.baro_altitude == -100.0