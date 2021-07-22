from tests.unit.repositories.mocked_cursor import MockedCursor
import pytest
from src.models.measure import Measure
from src.repositories.measure_repository import MeasureRepository
from src.utils.query_result import QueryResult
from datetime import datetime

mocked_cursor = MockedCursor()


def mocked_execute_query(query) -> QueryResult:
    mocked_cursor.executed_query = query
    query_result = QueryResult()
    query_result.from_cursor(mocked_cursor)
    return query_result


@pytest.fixture
def repository():
    repo = MeasureRepository()
    repo._execute_query = lambda query, transaction=None: mocked_execute_query(query)
    return repo


mocked_user_id = 5
mocked_ble_id = 5


def test_insert_adds_measure_to_measures_table(repository: MeasureRepository):
    mocked_cursor.prepare({})
    measure = Measure(1000000, 220.0, 1.0)
    repository.insert(measure, mocked_ble_id, mocked_user_id)
    assert 'insert into measures' in mocked_cursor.executed_query.lower()


def test_get_last_measures_returns_list_of_measures_from_last_time_interval_minutes(repository: MeasureRepository):
    now_date = datetime.now()
    mocked_cursor.prepare({'timestamp': [now_date], 'current': [1.5], 'voltage': [220.0]})
    measures = repository.get_last_measures('test_ble_id', 'test_user_id', 10)
    assert len(measures) == 1
    assert measures[0].timestamp == int(now_date.timestamp())
    assert measures[0].current == 1.5
    assert measures[0].voltage == 220.0
