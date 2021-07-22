import pytest
from src.controllers.auth_controller import AuthController
from src.models.user import User


@pytest.fixture
def controller():
    return AuthController()


def test_auth_controllers_instantiate_user_repository_when_instantiated(controller):
    assert controller.user_repository is not None


def test_create_returns_validation_error_when_user_in_json_body_is_not_valid(controller):
    controller.get_json_body = lambda: {
        'email': 'invalid_email', 'password': 'Passw0rd', 'username': 'Username'}
    actual = controller.register()
    assert actual.status_code == 400
    assert 'email' in actual.body['message']


def test_create_returns_error_when_user_with_same_email_already_exists(controller):
    controller.get_json_body = lambda: {
        'email': 'test@email.com', 'password': 'Passw0rd', 'username': 'Username', 'preferredLanguage': 'ES',
        'preferredCurrency': 'ARS'}
    controller.user_repository.email_exists = lambda x: True
    actual = controller.register()
    assert actual.status_code == 500
    assert actual.body['message'] == 'User with same email already exists'


def test_create_returns_error_when_can_not_insert_user_in_database(controller):
    controller.get_json_body = lambda: {
        'email': 'test@email.com', 'password': 'Passw0rd', 'username': 'Username'}
    controller.user_repository.email_exists = lambda x: False
    controller.user_repository.insert = lambda x: (
        _ for _ in ()).throw(Exception('Error'))
    actual = controller.register()
    assert actual.status_code == 500
    assert actual.body['message'] == 'An error has occurred while creating user'


def test_create_returns_ok_when_user_is_created(controller):
    controller.get_json_body = lambda: {
        'email': 'test@email.com', 'password': 'Passw0rd', 'username': 'Username'}
    controller.user_repository.email_exists = lambda x: False
    expected = 'new_user_id'
    controller.user_repository.insert = lambda x: expected
    actual = controller.register()
    assert actual.status_code == 201


def test_get_logged_user_data_returns_error_when_user_not_found(controller):
    controller.user_repository.get_by_id = lambda id, get_avatar: None
    actual = controller.get_logged_user_data()
    assert actual.status_code == 500
    assert actual.body['message'] == 'Invalid user'


def test_get_logged_user_data_returns_user_when_user_found(controller):
    user = User('test_username', 'test@test.com', user_id='user_id')
    controller.user_repository.get_by_id = lambda id, get_avatar: user
    actual = controller.get_logged_user_data()
    assert actual.status_code == 200
    assert actual.body['id'] == user.user_id
