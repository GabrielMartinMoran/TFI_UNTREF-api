import pytest
from src.common.hashing import hash_password
from src.domain.models.user import User
from tests.model_stubs.user_stub import UserStub


@pytest.fixture
def user_json():
    return {
        'username': 'username',
        'email': 'test@test.com',
        'password': 'Password',
    }


def test_is_valid_returns_false_when_username_is_none():
    user = UserStub(username=None)
    assert not user.is_valid()


def test_is_valid_returns_false_when_username_is_longer_than_32():
    user = UserStub(username='A' * 33)
    assert not user.is_valid()


def test_is_valid_returns_false_when_username_len_is_lower_than_3():
    user = UserStub(username='AA')
    assert not user.is_valid()


def test_is_valid_returns_false_when_email_is_null():
    user = UserStub(email=None)
    assert not user.is_valid()


def test_is_valid_returns_false_when_password_is_invalid():
    user = UserStub(password='invalidpassword')
    assert not user.is_valid()


def test_is_valid_returns_false_when_email_is_invalid():
    user = UserStub(email='invalidemail@invalid')
    assert not user.is_valid()


def test_is_valid_with_no_hashed_password_returns_false():
    user = UserStub(password=None, hashed_password=None)
    assert not user.is_valid()


def test_is_valid_returns_true_when_all_properties_are_valid():
    user = UserStub()
    assert user.is_valid()


def test_from_json_set_hashed_password_with_password_hashed_when_password_is_provided(user_json):
    user_json['password'] = "NEW_PASSWORD"
    actual = User.from_dict(user_json)
    assert actual.hashed_password == hash_password(user_json['password'])


def test_from_json_returns_user_when_json_is_provided(user_json):
    actual = User.from_dict(user_json)
    assert actual.username == user_json['username']
    assert actual.email == user_json['email']
    assert actual.hashed_password == hash_password(user_json['password'])


def test_password_matches_returns_true_when_hashed_password_is_equal_to_result_of_password_hashing():
    user = UserStub(password='Passw0rd')
    assert user.password_matches('Passw0rd')


def test_password_matches_returns_false_when_hashed_password_is_different_than_result_of_password_hashing():
    user = UserStub(password='Passw0rd')
    assert not user.password_matches('NotPassw0rd')
