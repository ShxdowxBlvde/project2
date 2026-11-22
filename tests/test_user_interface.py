
from unittest.mock import Mock, patch

import pytest

from src.user_interface import (
    get_top_n_by_altitude,
    get_by_origin_country,
    display_aeroplanes,
    run_user_interface,
)


def test_get_top_n_by_altitude(aeroplane_list):
    result = get_top_n_by_altitude(aeroplane_list, 1)

    assert len(result) == 1
    assert result[0].icao24 == "4ca123"
    assert result[0].baro_altitude == 11000.0


def test_get_top_n_by_altitude_returns_sorted_list(aeroplane_list):
    result = get_top_n_by_altitude(aeroplane_list, 2)

    assert result[0].baro_altitude >= result[1].baro_altitude


def test_get_top_n_excludes_none_altitude(
    aeroplane_list,
    aeroplane_factory,
):
    plane_without_altitude = aeroplane_factory(
        icao24="abcdef",
        baro_altitude=None,
    )

    planes = aeroplane_list + [plane_without_altitude]

    result = get_top_n_by_altitude(planes, 3)

    assert len(result) == 2
    assert all(plane.baro_altitude is not None for plane in result)


def test_get_top_n_invalid_count(aeroplane_list):
    with pytest.raises(ValueError):
        get_top_n_by_altitude(aeroplane_list, 0)


def test_get_top_n_negative_count(aeroplane_list):
    with pytest.raises(ValueError):
        get_top_n_by_altitude(aeroplane_list, -1)


def test_get_by_origin_country(aeroplane_list):
    result = get_by_origin_country(aeroplane_list, "Germany")

    assert len(result) == 1
    assert result[0].origin_country == "Germany"


def test_get_by_origin_country_case_insensitive(aeroplane_list):
    result = get_by_origin_country(aeroplane_list, "gErMaNy")

    assert len(result) == 1
    assert result[0].origin_country == "Germany"


def test_get_by_origin_country_not_found(aeroplane_list):
    result = get_by_origin_country(aeroplane_list, "France")

    assert result == []


def test_get_by_origin_country_empty_name(aeroplane_list):
    with pytest.raises(ValueError):
        get_by_origin_country(aeroplane_list, "   ")


def test_display_aeroplanes(aeroplane, capsys):
    display_aeroplanes([aeroplane])

    captured = capsys.readouterr()

    assert "3c675a" in captured.out
    assert "DLH123" in captured.out
    assert "Germany" in captured.out


def test_display_empty_list(capsys):
    display_aeroplanes([])

    captured = capsys.readouterr()

    assert "Самолёты не найдены" in captured.out


def test_run_user_interface_exit():
    api = Mock()
    saver = Mock()

    with patch("builtins.input", side_effect=["0"]):
        run_user_interface(api, saver)

    api.get_aeroplanes.assert_not_called()
    saver.add_aeroplanes.assert_not_called()


def test_run_user_interface_search_and_exit(aeroplane_list):
    api = Mock()
    saver = Mock()

    api.get_aeroplanes.return_value = aeroplane_list

    with patch(
        "builtins.input",
        side_effect=["Germany", "0"],
    ):
        run_user_interface(api, saver)

    api.get_aeroplanes.assert_called_once_with("Germany")
    saver.add_aeroplanes.assert_called_once_with(aeroplane_list)


def test_run_user_interface_empty_country():
    api = Mock()
    saver = Mock()

    with patch(
        "builtins.input",
        side_effect=["", "0"],
    ):
        run_user_interface(api, saver)

    api.get_aeroplanes.assert_not_called()
