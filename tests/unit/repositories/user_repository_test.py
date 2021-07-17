from src.utils.image_encoder import ImageEncoder
import requests
from tests.unit.repositories.mocked_cursor import MockedCursor
import pytest
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.utils.query_result import QueryResult

mocked_cursor = MockedCursor()


def mocked_execute_query(query) -> QueryResult:
    mocked_cursor.executed_query = query
    query_result = QueryResult()
    query_result.from_cursor(mocked_cursor)
    return query_result


@pytest.fixture
def repository():
    repo = UserRepository()
    repo._execute_query = lambda query, transaction=None: mocked_execute_query(query)
    return repo


expected_user_email = 'test@test.com'
expected_user_id = 5
expected_avatar = 'avatar_image'
expected_hashed_password = 'a48972f5646e654cb'
user_cursor_table = {'user_id': [expected_user_id], 'email': [expected_user_email]}


def test_get_by_email_returns_user_when_user_with_same_email_is_registered(repository: UserRepository):
    mocked_cursor.prepare(user_cursor_table)
    actual = repository.get_by_email(expected_user_email)
    assert expected_user_id == actual.user_id


def test_get_by_email_returns_none_when_user_with_provided_email_is_not_registered(repository: UserRepository):
    mocked_cursor.prepare({})
    actual = repository.get_by_email(expected_user_email)
    assert actual is None


def test_email_exists_returns_true_when_user_with_same_email_is_registered(repository: UserRepository):
    repository.get_by_email = lambda x: User('test_username', 'test@test.com')
    actual = repository.email_exists(expected_user_email)
    assert actual


def test_email_exists_returns_false_when_user_with_same_email_is_not_registered(repository: UserRepository):
    repository.get_by_email = lambda x: None
    actual = repository.email_exists(expected_user_email)
    assert not actual


def test_get_by_id_returns_user_when_user_with_same_id_exists(repository: UserRepository):
    mocked_cursor.prepare(user_cursor_table)
    actual = repository.get_by_id(expected_user_id)
    assert expected_user_id == actual.user_id


def test_get_by_id_returns_user_with_avatar_when_get_avatar_is_true_and_user_exists(repository: UserRepository):
    mocked_cursor.prepare(user_cursor_table)
    # Usamos el email para validar que llegue como parametro
    repository.get_user_avatar = lambda x: expected_avatar
    actual = repository.get_by_id(expected_user_id, get_avatar=True)
    assert expected_user_id == actual.user_id
    assert expected_avatar == actual.avatar


def test_get_user_avatar_returns_base64_avatar(repository: UserRepository):
    class Response:
        content = b'1'

    resp = Response()
    requests.get = lambda x: resp
    actual = repository.get_user_avatar(expected_user_email)
    assert ImageEncoder.BASE_64_ENCODING_PREFIX in actual


def test_insert_adds_user_to_users_table(repository: UserRepository):
    mocked_cursor.prepare({})
    user = User.from_dict({'id': expected_user_id, 'email': expected_user_email})
    repository.insert(user)
    assert 'insert into users'.lower() in mocked_cursor.executed_query.lower()


def test_get_returns_user_when_user_with_same_id_is_registered(repository: UserRepository):
    mocked_cursor.prepare(user_cursor_table)
    actual = repository.get(expected_user_id)
    assert expected_user_id == actual.user_id


def test_get_returns_none_when_user_with_provided_id_is_not_registered(repository: UserRepository):
    mocked_cursor.prepare({})
    actual = repository.get(expected_user_id)
    assert actual is None


def test_update_password_returns_true_when_could_update_user_with_provided_hashed_password(repository: UserRepository):
    mocked_cursor.prepare(affected_rows=1)
    actual = repository.update_password(expected_user_id, expected_hashed_password)
    assert actual


def test_update_password_returns_false_when_could_not_update_user_with_provided_hashed_password(
        repository: UserRepository):
    mocked_cursor.prepare(affected_rows=0)
    actual = repository.update_password(expected_user_id, expected_hashed_password)
    assert not actual
