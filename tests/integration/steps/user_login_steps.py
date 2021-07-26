from pytest_bdd import given, then, when, parsers

from src.app.controllers.auth_controller import AuthController
from src.app.utils.auth_info import AuthInfo
from src.app.utils.http.request import Request
from src.domain.models.user import User
from src.infrastructure.repositories.user_pg_repository import UserPGRepository
from tests.integration.utils import shared_variables


@given('user is logged in')
def user_is_logged_in():
    user_email = 'internal_tests_user@test.com'
    user_password = 'Passw0rd'
    user_repository = UserPGRepository()
    user = User(username=user_email, email=user_email, password=user_password)
    if not user_repository.exists(user.id):
        user_repository.create(user)

    auth_controller = AuthController(Request.from_body({
        'email': user_email,
        'password': user_password
    }))
    encoded_token = auth_controller.login().body['auth_info']
    shared_variables.logged_auth_info = AuthInfo.from_token(encoded_token)


@when(parsers.cfparse('user tries to login with email \'{email}\' and password \'{password}\''))
def try_user_login(email: str, password: str):
    controller = AuthController(Request.from_body({
        'email': email,
        'password': password
    }))
    shared_variables.last_response = controller.login()


@then('user logs in successfully')
def user_login_successfully():
    assert shared_variables.last_response.status_code == 200
    assert len(shared_variables.last_response.body['auth_info']) > 0


@then('user login fails')
def user_login_fails():
    assert shared_variables.last_response.status_code == 400
    assert shared_variables.last_response.body['message'] == 'Invalid email or password'
