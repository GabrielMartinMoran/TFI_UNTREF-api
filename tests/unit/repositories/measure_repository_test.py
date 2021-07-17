from tests.unit.repositories.mocked_cursor import MockedCursor
import pytest
from src.models.measure import Measure
from src.repositories.measure_repository import MeasureRepository
from src.utils.query_result import QueryResult


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