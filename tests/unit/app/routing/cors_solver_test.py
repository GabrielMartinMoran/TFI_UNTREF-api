from src.app.routing import cors_solver
from src.app.routing.cors_solver import CORSSolver
from src.app.utils.http import http_methods


class MockedRequest:
    def __init__(self, http_method: str, headers: dict = {}) -> None:
        self.method = http_method
        self.headers = headers


class MockedResponse:
    def __init__(self, ssuccess=True) -> None:
        self.ssuccess = ssuccess
        self.headers = {}


# Mockeamos el jsonify importado en cors_solver
cors_solver.jsonify = lambda ssuccess=True: MockedResponse(ssuccess)


def test_is_cors_request_returns_true_when_request_method_is_options():
    solver = CORSSolver(MockedRequest(http_methods.OPTIONS))
    assert solver.is_cors_request()


def test_is_cors_request_returns_false_when_request_method_is_not_options():
    solver = CORSSolver(MockedRequest(http_methods.POST))
    assert not solver.is_cors_request()


def test_get_wanted_http_method_returns_required_method_from_http_header():
    expected = http_methods.POST
    solver = CORSSolver(MockedRequest(http_methods.OPTIONS, {
        CORSSolver.REQUEST_METHOD_HEADER: expected
    }))
    actual = solver.get_wanted_http_metod()
    assert expected == actual


def test_get_cors_response_returns_http_cors_response_when_called():
    headers = {
        CORSSolver.REQUEST_METHOD_HEADER: http_methods.POST,
        CORSSolver.ORIGIN_HEADER: 'allow_origin_header',
        CORSSolver.REQUESTS_HEADERS_HEADER: 'request_headers'
    }
    solver = CORSSolver(MockedRequest(http_methods.OPTIONS, headers))
    actual = solver.get_cors_response()
    assert actual.ssuccess
    assert headers[CORSSolver.ORIGIN_HEADER] == actual.headers[CORSSolver.ALLOW_ORIGIN_HEADER]
    assert headers[CORSSolver.REQUEST_METHOD_HEADER] == actual.headers[CORSSolver.ALLOW_METHODS_HEADER]
    assert headers[CORSSolver.REQUESTS_HEADERS_HEADER] == actual.headers[CORSSolver.ALLOW_HEADERS_HEADER]
    assert CORSSolver.MAX_AGE == actual.headers[CORSSolver.MAX_AGE_HEADER]
    assert 'true' == actual.headers[CORSSolver.ALLOW_CREDENTIALS_HEADER]
