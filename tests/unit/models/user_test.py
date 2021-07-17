import pytest
from src.models.user import User
from src.utils.hashing import hash_password


@pytest.fixture
def user():
    user = User('username', 'test@test.com')
    user.hashed_password = hash_password('Passw0rd')
    return user

@pytest.fixture
def user_json():
    return {
        'id': '1234',
        'username': 'username',
        'email': 'test@test.com',
        'avatar': 'image_avatar',
        'createdDate': 'date',
        'password': 'Password',
    }

def test_is_valid_returns_false_when_username_is_null(user):
    user.username = None
    assert not user.is_valid()

def test_is_valid_returns_false_when_username_len_greater_than_32(user):
    user.username = "A" * 33
    assert not user.is_valid()

def test_is_valid_returns_false_when_username_len_is_lower_than_3(user):
    user.username = "AA"
    assert not user.is_valid()

def test_is_valid_returns_false_when_email_is_null(user):
    user.email = None
    assert not user.is_valid()

def test_is_valid_returns_false_when_password_is_invalid(user):
    user.password = 'invalidpassword'
    assert not user.is_valid()

def test_is_valid_returns_false_when_email_is_invalid(user):
    user.email = 'invalidemail@invalid'
    assert not user.is_valid()

def test_is_valid_with_no_hashed_password_returns_false(user):
    user.hashed_password = None
    assert not user.is_valid()

def test_is_valid_returns_true_when_all_properties_are_valid(user):
    assert user.is_valid()

def test_from_json_not_maps_created_date_when_not_provided(user_json):
    del user_json['createdDate']
    actual = User.from_dict(user_json)
    assert actual.created_date != 'date'

def test_from_json_set_hashed_password_with_password_hashed_when_password_is_provided(user_json):
    user_json['password'] = "NEW_PASSWORD"
    actual = User.from_dict(user_json)
    assert actual.hashed_password == hash_password(user_json['password'])

def test_from_json_returns_user_when_json_is_provided(user_json):
    actual = User.from_dict(user_json)
    assert actual.user_id == user_json['id']
    assert actual.username == user_json['username']
    assert actual.email == user_json['email']
    assert actual.hashed_password == hash_password(user_json['password'])
    assert actual.created_date == user_json['createdDate']

def test_password_matches_returns_true_when_hashed_password_is_equal_to_result_of_password_hashing(user):
    assert user.password_matches('Passw0rd')

def test_password_matches_returns_false_when_hashed_password_is_different_than_result_of_password_hashing(user):
    assert not user.password_matches('NotPassw0rd')