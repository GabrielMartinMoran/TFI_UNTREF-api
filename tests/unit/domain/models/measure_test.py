import pytest

from datetime import datetime

from src.domain.exceptions.model_validation_exception import ModelValidationException
from src.domain.mappers.measure_mapper import MeasureMapper
from src.domain.models.measure import Measure
from src.domain.serializers.measure_serializer import MeasureSerializer
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


def test_is_valid_raises_validation_exception_when_timestamp_is_none():
    expected = ['timestamp is not valid']
    with pytest.raises(ModelValidationException) as excinfo:
        MeasureStub(timestamp=None)
    assert excinfo.value.validation_errors == expected


def test_is_valid_raises_validation_exception_when_voltage_is_none():
    expected = ['voltage must be a valid float or int']
    with pytest.raises(ModelValidationException) as excinfo:
        MeasureStub(voltage=None)
    assert excinfo.value.validation_errors == expected


def test_is_valid_raises_validation_exception_when_voltage_is_lower_than_0():
    expected = ['voltage is not valid']
    with pytest.raises(ModelValidationException) as excinfo:
        MeasureStub(voltage=-1.0)
    assert excinfo.value.validation_errors == expected


def test_is_valid_raises_validation_exception_when_current_is_none():
    expected = ['current must be a valid float or int']
    with pytest.raises(ModelValidationException) as excinfo:
        MeasureStub(current=None)
    assert excinfo.value.validation_errors == expected


def test_is_valid_raises_validation_exception_when_current_is_lower_than_0():
    expected = ['current is not valid']
    with pytest.raises(ModelValidationException) as excinfo:
        MeasureStub(current=-1.0)
    assert excinfo.value.validation_errors == expected


def test_from_dict_instantiates_measure_with_provided_dict(measure_json):
    actual = MeasureMapper.map(measure_json)
    assert actual.timestamp == datetime.utcfromtimestamp(measure_json['timestamp'])
    assert actual.voltage == measure_json['voltage']
    assert actual.current == measure_json['current']


def test_to_dict_returns_measure_as_dict_when_called(measure):
    expected = {
        'current': 1.0,
        'power': 220.0,
        'timestamp': '1970-01-12T13:46:40+00:00',
        'voltage': 220.0
    }
    actual = MeasureSerializer.serialize(measure)
    assert actual == expected


def test_power_returns_measure_power_when_called():
    measure = MeasureStub(voltage=220.0, current=2.0)
    actual = measure.power
    assert actual == 440.0
