from pytest_bdd import given, then, when, parsers

from src.app.controllers.auth_controller import AuthController
from tests.integration.utils import shared_variables


@given('user is not registered')
def user_is_not_registered():
    pass


@given(parsers.cfparse('user with email \'{email}\' is already registered with password \'{password}\''))
def user_is_already_registered_with_password(email, password):
    try_register_user(email, email, password)


@given(parsers.cfparse('user with email \'{email}\' is already registered'))
def user_is_already_registered(email):
    try_register_user(email, email, 'Passw0rd')


@when(parsers.cfparse(
    'user tries to register with username \'{username}\', email \'{email}\' and password \'{password}\''))
def try_register_user(username, email, password):
    controller = AuthController()
    controller.get_json_body = lambda: {
        'username': username,
        'email': email,
        'password': password
    }
    shared_variables.last_response = controller.register()


@then('user registers successfully')
def user_register_successfully():
    assert shared_variables.last_response.status_code == 201


@then(parsers.cfparse('error is \'{message}\''))
def error_is_password_is_not_valid(message):
    assert message in shared_variables.last_response.body['message']


@then('user registration fails')
def user_register_fails():
    assert shared_variables.last_response.status_code != 201
