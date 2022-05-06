import pytest
from src.common.hashing import hash_password
from src.domain.exceptions.model_validation_exception import ModelValidationException
from src.domain.models.user import User
from tests.model_stubs.user_stub import UserStub


@pytest.fixture
def user_json():
    return {
        'username': 'username',
        'email': 'test@test.com',
        'password': 'Pa$$w0rd',
    }


def test_is_valid_raises_validation_exception_when_username_is_none():
    expected = ['username is not valid']
    with pytest.raises(ModelValidationException) as excinfo:
        UserStub(username=None)
    assert excinfo.value.validation_errors == expected


def test_is_valid_raises_validation_exception_when_username_is_longer_than_32():
    expected = ['username is not valid']
    with pytest.raises(ModelValidationException) as excinfo:
        UserStub(username='A' * 33)
    assert excinfo.value.validation_errors == expected


def test_is_valid_raises_validation_exception_when_username_len_is_lower_than_3():
    expected = ['username is not valid']
    with pytest.raises(ModelValidationException) as excinfo:
        UserStub(username='AA')
    assert excinfo.value.validation_errors == expected


def test_is_valid_raises_validation_exception_when_email_is_null():
    expected = ['email is not valid']
    with pytest.raises(ModelValidationException) as excinfo:
        UserStub(email=None)
    assert excinfo.value.validation_errors == expected


def test_is_valid_raises_validation_exception_when_email_is_invalid():
    expected = ['email is not valid']
    with pytest.raises(ModelValidationException) as excinfo:
        UserStub(email='invalidemail@invalid')
    assert excinfo.value.validation_errors == expected


def test_is_valid_raises_validation_exception_when_password_is_invalid():
    expected = ['password is not valid']
    with pytest.raises(ModelValidationException) as excinfo:
        UserStub(password='invalidpassword')
    assert excinfo.value.validation_errors == expected


def test_is_valid_with_no_hashed_password_raises_validation_exception():
    expected = ['password is not valid']
    with pytest.raises(ModelValidationException) as excinfo:
        UserStub(password=None, hashed_password=None)
    assert excinfo.value.validation_errors == expected


def test_from_json_set_hashed_password_with_password_hashed_when_password_is_provided(user_json):
    user_json['password'] = 'New_PA$$W0RD'
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
