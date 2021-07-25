import pytest

from datetime import datetime
from src.domain.models.measure import Measure
from tests.model_stubs.measure_stub import MeasureStub


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


def test_is_valid_returns_false_when_timestamp_is_none():
    measure = MeasureStub(timestamp=None)
    assert not measure.is_valid()


def test_is_valid_returns_false_when_voltage_is_none():
    measure = MeasureStub(voltage=None)
    assert not measure.is_valid()


def test_is_valid_returns_false_when_voltage_is_lower_than_0():
    measure = MeasureStub(voltage=-1.0)
    assert not measure.is_valid()


def test_is_valid_returns_false_when_current_is_none():
    measure = MeasureStub(current=None)
    assert not measure.is_valid()


def test_is_valid_returns_false_when_current_is_lower_than_0():
    measure = MeasureStub(current=-1.0)
    assert not measure.is_valid()


def test_is_valid_returns_true_when_all_properties_are_valid():
    measure = MeasureStub()
    assert measure.is_valid()


def test_from_dict_instantiates_measure_with_provided_dict(measure_json):
    actual = Measure.from_dict(measure_json)
    assert actual.timestamp == datetime.utcfromtimestamp(measure_json['timestamp'])
    assert actual.voltage == measure_json['voltage']
    assert actual.current == measure_json['current']


def test_to_dict_returns_measure_as_dict_when_called(measure):
    actual = measure.to_dict()
    assert actual == {
        'timestamp': measure.timestamp.isoformat(),
        'voltage': measure.voltage,
        'current': measure.current,
        'power': measure.voltage * measure.current
    }


def test_power_returns_measure_power_when_called():
    measure = MeasureStub(voltage=220.0, current=2.0)
    actual = measure.power
    assert actual == 440.0
