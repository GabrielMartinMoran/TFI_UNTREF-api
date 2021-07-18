import pytest
from src.models.device import Device
from src.models.measure import Measure


@pytest.fixture
def device():
    device = Device(
        'device_name',
        'e348ae42-ebb0-4453-a12f-c05bdadd1479',
        device_id='1234',
        active=True,
        turned_on=True
    )
    device.measures = [Measure(timestamp=10000, voltage=220.0, current=1.0)]
    return device


@pytest.fixture
def device_json():
    return {
        'id': '1234',
        'name': 'device_name',
        'ble_id': 'e348ae42-ebb0-4453-a12f-c05bdadd1479',
        'active': True,
        'turned_on': True,
        'created_date': 'date',
        'measures': [{
            'timestamp': 10000,
            'voltage': 220.0,
            'current': 1.0
        }]
    }


def test_is_valid_returns_false_when_name_is_null(device):
    device.name = None
    assert not device.is_valid()


def test_is_valid_returns_false_when_name_len_greater_than_32(device):
    device.name = 'A' * 33
    assert not device.is_valid()


def test_is_valid_returns_false_when_name_len_is_lower_than_1(device):
    device.name = ''
    assert not device.is_valid()


def test_is_valid_returns_false_when_ble_id_is_null(device):
    device.ble_id = None
    assert not device.is_valid()


def test_is_valid_returns_false_when_ble_id_is_invalid(device):
    device.ble_id = 'invalid_ble_id'
    assert not device.is_valid()


def test_is_valid_returns_true_when_all_properties_are_valid(device):
    assert device.is_valid()


def test_from_json_returns_device_when_json_is_provided(device_json):
    actual = Device.from_dict(device_json)
    assert actual.device_id == device_json['id']
    assert actual.name == device_json['name']
    assert actual.ble_id == device_json['ble_id']
    assert actual.active == device_json['active']
    assert actual.turned_on == device_json['turned_on']
    assert actual.created_date == device_json['created_date']
    assert actual.measures[0].timestamp == device_json['measures'][0]['timestamp']
    assert actual.measures[0].voltage == device_json['measures'][0]['voltage']
    assert actual.measures[0].current == device_json['measures'][0]['current']


def test_to_json_returns_device_as_json_when_called(device):
    actual = device.to_dict()
    assert actual['id'] == device.device_id
    assert actual['name'] == device.name
    assert actual['ble_id'] == device.ble_id
    assert actual['active'] == device.active
    assert actual['turned_on'] == device.turned_on
    assert actual['measures'][0]['timestamp'] == device.measures[0].timestamp
    assert actual['measures'][0]['voltage'] == device.measures[0].voltage
    assert actual['measures'][0]['current'] == device.measures[0].current
