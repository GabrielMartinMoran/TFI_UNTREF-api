from pytest_bdd import then, when, parsers

from src.app.controllers.auth_controller import AuthController
from src.app.utils.auth.device_token import DeviceToken
from src.app.utils.http.request import Request
from tests.integration.utils import shared_variables


@when(parsers.cfparse('user tries to generate a token for device with id \'{device_id}\''))
def try_generate_device_token(device_id: str):
    controller = AuthController(request=Request(None, None, {}, {}), token=shared_variables.token)
    shared_variables.last_response = controller.generate_device_token(device_id)


@then('device token is returned successfully')
def device_token_returned_successfully():
    token = shared_variables.last_response.body['token']
    assert shared_variables.last_response.status_code == 200
    assert len(token) > 0
    assert DeviceToken.is_encoded_form(token)
