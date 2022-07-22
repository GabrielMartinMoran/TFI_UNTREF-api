import pytest
from src.app.routing.controller_route import ControllerRoute


class MockedController:
    pass


@pytest.fixture
def controller_route():
    return ControllerRoute(MockedController)


def test_add_method_adds_method_route_to_methods_when_called(controller_route):
    expected = 'controller_method'
    controller_route.add_method(expected, 'POST', 'method_alias', False)
    assert 1 == len(controller_route.methods)
    assert expected == controller_route.methods[0].method_name


def test_route_returs_controller_class_name_lowercase_without_controller_sufix_when_called(controller_route):
    actual = controller_route.route()
    assert 'mocked' == actual


def test_controller_name_returns_controller_class_name_as_string_when_called(controller_route):
    actual = controller_route.controller_name()
    assert MockedController.__name__ == actual
