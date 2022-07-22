from pytest_bdd import then, when

from src.app.controllers.auth_controller import AuthController
from tests.integration.utils import shared_variables


@when('user tries to get his data')
def try_get_user_data():
    controller = AuthController(None, shared_variables.logged_auth_info)
    shared_variables.last_response = controller.get_logged_user_data()


@then('user data is returned')
def user_data_returned():
    assert shared_variables.last_response.status_code == 200
    assert shared_variables.last_response.body['email'] == shared_variables.logged_auth_info.user_email
    assert len(shared_variables.last_response.body['username']) > 0
