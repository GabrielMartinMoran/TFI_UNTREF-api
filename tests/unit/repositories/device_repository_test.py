from tests.unit.repositories.mocked_cursor import MockedCursor
import pytest
from src.models.device import Device
from src.repositories.device_repository import DeviceRepository
from src.utils.query_result import QueryResult

mocked_cursor = MockedCursor()


def mocked_execute_query(query) -> QueryResult:
    mocked_cursor.executed_query = query
    query_result = QueryResult()
    query_result.from_cursor(mocked_cursor)
    return query_result


@pytest.fixture
def repository():
    repo = DeviceRepository()
    repo._execute_query = lambda query, transaction=None: mocked_execute_query(query)
    return repo


mocked_user_id = 5
mocked_ble_id = 5
expected_device_id = 25


def test_insert_adds_user_to_devices_table(repository: DeviceRepository):
    mocked_cursor.prepare({'device_id': [expected_device_id]})
    device = Device('device_name', 'e348ae42-ebb0-4453-a12f-c05bdadd1479')
    actual = repository.insert(device, mocked_user_id)
    assert expected_device_id == actual


def test_ble_id_exists_for_user_returns_true_when_device_with_same_ble_id_and_user_id_exists(
        repository: DeviceRepository):
    mocked_cursor.prepare({'count': [1]})
    actual = repository.ble_id_exists_for_user(mocked_ble_id, mocked_user_id)
    assert actual


def test_ble_id_exists_for_user_returns_false_when_device_with_same_ble_id_and_user_id_does_not_exist(
        repository: DeviceRepository):
    mocked_cursor.prepare({'count': [0]})
    actual = repository.ble_id_exists_for_user(mocked_ble_id, mocked_user_id)
    assert not actual
