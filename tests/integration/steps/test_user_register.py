from pytest_bdd import given, scenarios, then, when, parsers

from src.controllers.auth_controller import AuthController

scenarios('../features/user_register.feature')

last_response = None


@given('user is not registered')
def user_is_not_registered():
    pass


@given(parsers.cfparse('user with email \'{email}\' is already registered'))
def user_is_already_registered(email):
    try_register_user(email, email, 'Passw0rd')


@when(
    parsers.cfparse(
        'user tries to register with username \'{username}\', email \'{email}\' and password \'{password}\''
    )
)
def try_register_user(username, email, password):
    controller = AuthController()
    controller.get_json_body = lambda: {
        'username': username,
        'email': email,
        'password': password
    }
    global last_response
    last_response = controller.register()


@then('user registers successfully')
def user_register_successfully():
    global last_response
    assert last_response.status_code == 201


@then(parsers.cfparse('error is \'{message}\''))
def error_is_password_is_not_valid(message):
    global last_response
    assert message in last_response.body['message']


@then('user registration fails')
def user_register_fails():
    global last_response
    assert last_response.status_code != 201
