import requests
from unittest.mock import Mock, patch

import pytest

from src.api import NominatimAPI, OpenSkyAPI, AeroplanesAPI
from src.aeroplane import Aeroplane

# NominatimAPI


@patch("src.api.requests.get")
def test_nominatim_get_data(mock_get):
    expected_data = [{"boundingbox": ["50.0", "55.0", "5.0", "10.0"]}]

    mock_response = Mock()
    mock_response.json.return_value = expected_data
    mock_get.return_value = mock_response

    api = NominatimAPI()
    result = api.get_data({"country": "Germany"})

    assert result == expected_data
    mock_get.assert_called_once_with(
        api.base_url,
        params={"country": "Germany"},
        headers=api.headers,
        timeout=10,
    )
    mock_response.raise_for_status.assert_called_once()


@patch("src.api.requests.get")
def test_nominatim_http_error(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP error")
    mock_get.return_value = mock_response

    api = NominatimAPI()

    with pytest.raises(__import__("requests").HTTPError):
        api.get_data({"country": "Germany"})


# OpenSkyAPI


@patch("src.api.requests.get")
def test_opensky_get_data(mock_get):
    expected_data = {"states": []}

    mock_response = Mock()
    mock_response.json.return_value = expected_data
    mock_get.return_value = mock_response

    api = OpenSkyAPI()
    result = api.get_data({"lamin": 50.0})

    assert result == expected_data
    mock_get.assert_called_once_with(
        api.base_url,
        params={"lamin": 50.0},
        headers=api.headers,
        timeout=10,
    )
    mock_response.raise_for_status.assert_called_once()


@patch("src.api.requests.get")
def test_opensky_http_error(mock_get):
    import requests

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP error")
    mock_get.return_value = mock_response

    api = OpenSkyAPI()

    with pytest.raises(requests.HTTPError):
        api.get_data({"lamin": 50.0})


# AeroplanesAPI


def test_get_aeroplanes(aeroplane):
    api = AeroplanesAPI()

    api.nominatim.get_data = Mock(
        return_value=[{"boundingbox": ["50.0", "55.0", "5.0", "10.0"]}]
    )

    api.opensky.get_data = Mock(return_value={"states": []})

    result = api.get_aeroplanes("Germany")

    assert result == []
    api.nominatim.get_data.assert_called_once_with(
        {
            "country": "Germany",
            "format": "json",
            "limit": 1,
        }
    )
    api.opensky.get_data.assert_called_once_with(
        {
            "lamin": 50.0,
            "lamax": 55.0,
            "lomin": 5.0,
            "lomax": 10.0,
        }
    )


def test_get_aeroplanes_returns_objects(aeroplane):
    api = AeroplanesAPI()

    api.nominatim.get_data = Mock(
        return_value=[{"boundingbox": ["50.0", "55.0", "5.0", "10.0"]}]
    )

    api.opensky.get_data = Mock(
        return_value={
            "states": [
                [
                    "3c675a",
                    "DLH123",
                    "Germany",
                    None,
                    None,
                    None,
                    None,
                    10000.0,
                    None,
                    250.0,
                    None,
                    0.0,
                ]
            ]
        }
    )

    result = api.get_aeroplanes("Germany")

    assert len(result) == 1
    assert isinstance(result[0], Aeroplane)
    assert result[0].icao24 == "3c675a"


def test_get_aeroplanes_without_geo_data():
    api = AeroplanesAPI()
    api.nominatim.get_data = Mock(return_value=[])

    with pytest.raises(ValueError):
        api.get_aeroplanes("Unknown country")


def test_get_aeroplanes_without_boundingbox():
    api = AeroplanesAPI()
    api.nominatim.get_data = Mock(return_value=[{"display_name": "Germany"}])

    with pytest.raises(ValueError):
        api.get_aeroplanes("Germany")
