import pytest
from src.utils import global_variables
from src.routing.router import Router
from src.routing import router
from src.routing import cors_solver
import jwt
from src import config

class MockedRequest:
    def __init__(self, http_method: str, headers: dict={}) -> None:
        self.method = http_method
        self.headers = headers

class MockedResponse:
    def __init__(self, body, code) -> None:
        self.body = body
        self.code = code
        self.headers = {}

class MockedController:

    def __init__(self):
        self.request = None
        self.token = None
        self.response = None

    def mocked_http_endpoint(self):
        return MockedResponse({ 'message': 'OK'}, 200)

    def mocked_http_endpoint_with_params(self, param1, param2):
        return MockedResponse({ 'param1': param1, 'param2': param2}, 200)

    def mocked_http_endpoint_with_auth_required(self):
        return MockedResponse({ 'message': 'OK'}, 200)

    def mocked_http_endpoint_that_raises_exception(self):
        raise Exception("Mocked error")

    def on_request(self):
        pass

    def after_request(self):
        pass

def discover_controllers_mocked(router_instance):
    Router.register_http_method({
        'type': 'POST', 'alias': None,'class_name': 'MockedController', 'method_name': 'mocked_http_endpoint', 'auth_required': False
    })
    Router.register_http_method({
        'type': 'GET', 'alias': None,'class_name': 'MockedController', 'method_name': 'mocked_http_endpoint_with_params', 'auth_required': False
    })
    Router.register_http_method({
        'type': 'GET', 'alias': None,'class_name': 'MockedController', 'method_name': 'mocked_http_endpoint_with_auth_required', 'auth_required': True
    })
    Router.register_http_method({
        'type': 'GET', 'alias': None,'class_name': 'MockedController', 'method_name': 'mocked_http_endpoint_that_raises_exception', 'auth_required': False
    })
    return [MockedController]

def create_token(token_data: dict):
    return 'Bearer ' + jwt.encode(token_data, config.APP_SECRET, algorithm=config.HASH_ALGORITHM)

# Mockeamos la funcion make_response importado desde flask
router.make_response = lambda message, code: MockedResponse(message, code)


@pytest.fixture
def router():
    Router._Router__discover_controllers = discover_controllers_mocked
    return Router()

def test_router_register_router_instance_in_global_variables_when_instantiated():
    router = Router()
    assert router == global_variables.ROUTER_INSTANCE

def test_router_map_rutes_when_instantiated():
    Router._Router__discover_controllers = discover_controllers_mocked
    router = Router()
    assert 1 == len(router.routes)
    assert MockedController == router.routes[0].controller_class
    assert 'mocked_http_endpoint' == router.routes[0].methods[0].method_name
    assert 'POST' == router.routes[0].methods[0].http_type
    assert None == router.routes[0].methods[0].alias
    assert not router.routes[0].methods[0].auth_required

def test_route_returns_error_response_when_controller_is_not_in_path(router):
    request = MockedRequest('POST', {})
    actual = router.route(request, '')
    assert actual.body['message'] == 'Not found'
    assert actual.code == 404

def test_route_returns_error_response_when_method_is_not_in_path(router):
    request = MockedRequest('POST')
    actual = router.route(request, 'mocked')
    assert actual.body['message'] == 'Not found'
    assert actual.code == 404

def test_route_returns_error_response_when_method_is_valid_but_http_method_type_does_not_match(router):
    request = MockedRequest('GET')
    actual = router.route(request, 'mocked')
    assert actual.body['message'] == 'Not found'
    assert actual.code == 404

def test_route_executes_controller_method_when_route_is_valid(router):
    param1 = 'text_param'
    param2 = 10
    request = MockedRequest('GET')
    actual = router.route(request, f'mocked/mocked_http_endpoint_with_params/{param1}/{param2}')
    assert actual.body['param1'] == param1
    assert actual.body['param2'] == str(param2)
    assert actual.code == 200

def test_route_returns_error_response_when_endpoint_is_valid_but_params_are_invalid(router):
    request = MockedRequest('GET')
    actual = router.route(request, 'mocked/mocked_http_endpoint_with_params')
    assert actual.body['message'] == 'Bad method arguments'
    assert actual.code == 400

def test_route_returns_error_response_when_mapped_method_raises_exception(router):
    request = MockedRequest('GET')
    actual = router.route(request, 'mocked/mocked_http_endpoint_that_raises_exception')
    assert actual.body['message'] == 'Internal server error'
    assert actual.code == 500

def test_route_returns_error_response_when_cors_wanted_method_is_not_valid(router):
    request = MockedRequest('OPTIONS', {
        'Origin': 'local',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': None
    })
    actual = router.route(request, 'mocked/invalid_http_endpoint')
    assert actual.body['message'] == 'Not found'
    assert actual.code == 404

def test_route_returns_cors_response_when_cors_requested_in_valid_endpoint(router):
    # Mockeamos el jsonify importado en cors_solver
    cors_solver.jsonify = lambda ssuccess=True: MockedResponse({}, 200)
    request = MockedRequest('OPTIONS', {
        'Origin': 'local',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': None
    })
    actual = router.route(request, 'mocked/mocked_http_endpoint')
    assert actual.headers['Access-Control-Allow-Methods'] == 'POST'
    assert actual.code == 200

def test_route_returns_error_response_when_token_required_and_not_provided(router):
    request = MockedRequest('GET')
    actual = router.route(request, 'mocked/mocked_http_endpoint_with_auth_required')
    assert actual.body['message'] == 'Unauthorized'
    assert actual.code == 401

def test_route_returns_ok_response_when_token_required_and_provided(router):
    request = MockedRequest('GET', {'Authorization': create_token({'username': 'test_user'})})
    actual = router.route(request, 'mocked/mocked_http_endpoint_with_auth_required')
    assert actual.body['message'] == 'OK'
    assert actual.code == 200

def test_get_base_url_returns_base_api_url_when_called():
    actual = Router.get_base_url()
    assert 'api' == actual