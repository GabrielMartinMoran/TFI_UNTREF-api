import pytest
from src.domain.models.device import Device
from src.domain.models.measure import Measure
from tests.model_stubs.device_stub import DeviceStub


@pytest.fixture
def device():
    device = Device(
        'device_name',
        'e348ae42-ebb0-4453-a12f-c05bdadd1479',
        active=True,
        turned_on=True,
        measures=[Measure(timestamp=10000, voltage=220.0, current=1.0)]
    )
    return device


@pytest.fixture
def device_json():
    return {
        'name': 'device_name',
        'id': 'e348ae42-ebb0-4453-a12f-c05bdadd1479',
        'active': True,
        'turned_on': True,
        'created_date': 'date',
        'measures': [{
            'timestamp': 10000,
            'voltage': 220.0,
            'current': 1.0
        }]
    }


def test_is_valid_returns_false_when_name_is_null():
    device = DeviceStub(name=None)
    assert not device.is_valid()


def test_is_valid_returns_false_when_name_len_greater_than_32(device):
    device = DeviceStub(name='A' * 33)
    assert not device.is_valid()


def test_is_valid_returns_false_when_name_len_zero(device):
    device = DeviceStub(name='')
    assert not device.is_valid()


def test_is_valid_returns_false_when_id_is_invalid():
    device = DeviceStub(device_id='invalid_device_id')
    assert not device.is_valid()


def test_is_valid_returns_true_when_all_properties_are_valid(device):
    assert device.is_valid()


def test_from_dict_instantiates_device_from_provided_dict(device_json):
    actual = Device.from_dict(device_json)
    assert actual.id == device_json['id']
    assert actual.name == device_json['name']
    assert actual.active == device_json['active']
    assert actual.turned_on == device_json['turned_on']
    assert actual.created_date == device_json['created_date']
    assert actual.measures[0].timestamp.timestamp() == device_json['measures'][0]['timestamp']
    assert actual.measures[0].voltage == device_json['measures'][0]['voltage']
    assert actual.measures[0].current == device_json['measures'][0]['current']


def test_to_dict_returns_device_as_dict_when_called(device):
    actual = device.to_dict()
    assert actual['id'] == device.id
    assert actual['name'] == device.name
    assert actual['active'] == device.active
    assert actual['turned_on'] == device.turned_on
    assert actual['measures'][0]['timestamp'] == device.measures[0].timestamp.isoformat()
    assert actual['measures'][0]['voltage'] == device.measures[0].voltage
    assert actual['measures'][0]['current'] == device.measures[0].current
