from tests.unit.repositories.mocked_cursor import MockedCursor
import pytest
from src.repositories.base_repository import BaseRepository
from src.repositories import base_repository


class MockedTransaction:

    def __init__(self) -> None:
        self.commited = False
        self.rollbacked = False
        self.closed = False

    def cursor(self):
        return mocked_cursor

    def commit(self):
        self.commited = True

    def rollback(self):
        self.rollbacked = True

    def close(self):
        self.closed = True


mocked_cursor = MockedCursor()
mocked_transaction = MockedTransaction()

mocked_query = 'SELECT * FROM Mocked'


def create_transaction() -> MockedTransaction:
    global mocked_transaction
    mocked_transaction = MockedTransaction()
    return mocked_transaction


@pytest.fixture
def repository():
    repo = BaseRepository()
    # repo._execute_query = lambda query, transaction=None: mocked_execute_query(query)
    return repo


def test_execute_query_creates_trasaction_when_not_provided(repository: BaseRepository):
    global mocked_transaction
    mocked_transaction = None
    repository._create_transaction = create_transaction
    mocked_cursor.prepare()
    repository._execute_query(mocked_query)
    assert mocked_transaction is not None
    assert mocked_transaction.commited
    assert mocked_transaction.closed
    assert mocked_query == mocked_cursor.executed_query


def test_execute_query_rollback_connection_when_error_occured_and_transaction_not_provided(repository: BaseRepository):
    global mocked_transaction
    mocked_transaction = None
    repository._create_transaction = create_transaction
    mocked_cursor.prepare(execute_raises_exception=True)
    with pytest.raises(Exception):
        repository._execute_query(mocked_query)
    assert mocked_transaction is not None
    assert mocked_transaction.rollbacked
    assert mocked_transaction.closed
    assert mocked_query == mocked_cursor.executed_query


def test_execute_query_uses_existing_transaction_if_provided(repository: BaseRepository):
    global mocked_transaction
    mocked_transaction = MockedTransaction()
    mocked_cursor.prepare()
    repository._execute_query(mocked_query, mocked_transaction)
    assert not mocked_transaction.commited
    assert not mocked_transaction.closed
    assert mocked_query == mocked_cursor.executed_query


def test_execute_query_noes_not_rollback_connection_when_error_occured_and_transaction_provided(
        repository: BaseRepository):
    global mocked_transaction
    mocked_transaction = MockedTransaction()
    mocked_cursor.prepare(execute_raises_exception=True)
    with pytest.raises(Exception):
        repository._execute_query(mocked_query, mocked_transaction)
    assert not mocked_transaction.rollbacked
    assert not mocked_transaction.closed
    assert mocked_query == mocked_cursor.executed_query


def test_create_transaction_creates_db_connection(repository: BaseRepository):
    psycopg2_connect = base_repository.psycopg2.connect
    base_repository.psycopg2.connect = lambda conn_string: conn_string
    actual = repository._create_transaction()
    base_repository.psycopg2.connect = psycopg2_connect
    assert 'user' in actual
    assert 'password' in actual
    assert 'host' in actual
    assert 'port' in actual
    assert 'dbname' in actual
