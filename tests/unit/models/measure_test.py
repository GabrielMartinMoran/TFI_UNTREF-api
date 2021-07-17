import pytest
from src.models.measure import Measure


@pytest.fixture
def measure():
    return Measure(1000000, 220.0, 1.0)


@pytest.fixture
def measure_json():
    return {
        'timestamp': 1000000,
        'voltage': 220.0,
        'current': 1.0
    }


def test_is_valid_returns_false_when_timestamp_null(measure):
    measure.timestamp = None
    assert not measure.is_valid()


def test_is_valid_returns_false_when_timestamp_is_lower_than_0(measure):
    measure.timestamp = -1
    assert not measure.is_valid()


def test_is_valid_returns_false_when_timestamp_is_not_int(measure):
    measure.timestamp = '1000'
    assert not measure.is_valid()


def test_is_valid_returns_false_when_voltage_is_none(measure):
    measure.voltage = None
    assert not measure.is_valid()


def test_is_valid_returns_false_when_voltage_is_lower_than_0(measure):
    measure.voltage = -1.0
    assert not measure.is_valid()


def test_is_valid_returns_false_when_voltage_is_not_float(measure):
    measure.voltage = 220
    assert not measure.is_valid()


def test_is_valid_returns_false_when_current_is_none(measure):
    measure.current = None
    assert not measure.is_valid()


def test_is_valid_returns_false_when_current_is_lower_than_0(measure):
    measure.current = -1.0
    assert not measure.is_valid()


def test_is_valid_returns_false_when_current_is_not_float(measure):
    measure.current = 1
    assert not measure.is_valid()


def test_is_valid_returns_true_when_all_properties_are_valid(measure):
    assert measure.is_valid()


def test_from_json_returns_measure_when_json_is_provided(measure_json):
    actual = Measure.from_dict(measure_json)
    assert actual.timestamp == measure_json['timestamp']
    assert actual.voltage == measure_json['voltage']
    assert actual.current == measure_json['current']


def test_to_json_returns_measure_as_json_when_called(measure):
    actual = measure.to_dict()
    assert actual['timestamp'] == measure.timestamp
    assert actual['voltage'] == measure.voltage
    assert actual['current'] == measure.current
