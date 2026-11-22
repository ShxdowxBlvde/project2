import pytest

from src.base_api import BaseAPI


def test_base_api_is_abstract():
    with pytest.raises(TypeError):
        BaseAPI("https://example.com", {})
