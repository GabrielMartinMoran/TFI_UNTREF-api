import pytest
from src.routing.method_route import MethodRoute

@pytest.fixture
def method_route():
    return MethodRoute("class", "method", "http_type", "method_alias", False)


def test_get_path_returns_alias_when_alias_is_not_none(method_route):
    actual = method_route.get_path()
    assert method_route.alias == actual

def test_get_path_returns_method_name_as_route_when_alias_is_none(method_route):
    method_route.alias = None
    expected = F'/{method_route.method_name}'
    actual = method_route.get_path()
    assert expected == actual