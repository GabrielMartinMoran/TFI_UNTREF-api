from src.app.controllers.devices_controller import DevicesController
from src.app.utils.http.request import Request
from src.domain.models.device import Device
from src.domain.models.measure import Measure
from tests.model_stubs.measure_stub import MeasureStub


def test_device_controller_instantiate_device_repository_when_instantiated():
    controller = DevicesController(None)
    assert controller.device_repository is not None


def test_device_controller_instantiate_measure_repository_when_instantiated():
    controller = DevicesController(None)
    assert controller.measure_repository is not None


"""
def test_generate_ble_id_generates_unique_ble_id():
    controller = DevicesController(None)
    actual = controller.generate_ble_id()
    assert actual.status_code == 200
    assert isinstance(actual.body['device_id'], str)
"""


def test_create_returns_error_response_when_device_is_not_valid():
    controller = DevicesController(Request.from_body({'name': None}))
    actual = controller.create()
    assert actual.status_code == 400
    assert 'Validation error' in actual.body['message']


def test_create_returns_error_response_when_device_with_same_ble_id_exists_for_user():
    controller = DevicesController(
        Request.from_body({'name': 'test_device', 'device_id': '5c7b5ffc-90e7-1b85-f041-0595c912c905'}))
    controller.device_repository.exists_for_user = lambda ble_id, user_id: True
    actual = controller.create()
    assert actual.status_code == 409
    assert actual.body['message'] == 'There is another device with the same device_id for logged user'


def test_create_returns_ok_response_when_device_was_created_successfully():
    controller = DevicesController(Request.from_body({'name': 'test_device'}))
    controller.device_repository.exists_for_user = lambda device_id, user_id: False
    controller.device_repository.create = lambda device, user_id: device.id
    actual = controller.create()
    assert actual.status_code == 201
    assert isinstance(actual.body['id'], str)


def test_add_measure_returns_error_response_when_measure_is_not_valid():
    measure = MeasureStub(current=None)
    controller = DevicesController(Request.from_body({
        'timestamp': measure.timestamp.isoformat(),
        'voltage': measure.voltage,
        'current': None
    }))
    actual = controller.add_measure('5c7b5ffc-90e7-1b85-f041-0595c912c905')
    assert actual.status_code == 400
    assert 'Validation error' in actual.body['message']


def test_add_measure_returns_error_response_when_device_is_not_valid_for_user():
    controller = DevicesController(Request.from_body(MeasureStub().to_dict()))
    controller.device_repository.exists_for_user = lambda ble_id, user_id: False
    actual = controller.add_measure('5c7b5ffc-90e7-1b85-f041-0595c912c905')
    assert actual.status_code == 400
    assert actual.body['message'] == 'Device identifier is not valid for logged user'


def test_add_measure_returns_ok_response_when_measure_was_registered():
    controller = DevicesController(Request.from_body(MeasureStub().to_dict()))
    controller.device_repository.exists_for_user = lambda device_id, user_id: True
    controller.measure_repository.create = lambda measure, device_id: None
    actual = controller.add_measure('5c7b5ffc-90e7-1b85-f041-0595c912c905')
    assert actual.status_code == 201
    assert actual.body == {}


def test_measures_returns_error_response_when_device_is_not_valid_for_user():
    controller = DevicesController(None)
    controller.device_repository.exists_for_user = lambda ble_id, user_id: False
    actual = controller.get_measures('5c7b5ffc-90e7-1b85-f041-0595c912c905', 5)
    assert actual.status_code == 400
    assert actual.body['message'] == 'Device identifier is not valid for logged user'


def test_measures_returns_ok_response_when_could_summarize_measures():
    controller = DevicesController(None)
    controller.device_repository.exists_for_user = lambda device_id, user_id: True
    controller.measure_repository.get_from_last_minutes = lambda device_id, time_interval: [
        Measure(1626551296, 220.571, 5.432),
        Measure(1626551301, 220.424, 5.555),
        Measure(1626551306, 219.4, 5.512),
        Measure(1626551311, 218.93, 5.628),
        Measure(1626551316, 219.157, 5.579),
        Measure(1626551321, 222.171, 5.656),
        Measure(1626551326, 219.634, 5.696),
        Measure(1626551331, 217.96, 5.449),
        Measure(1626551336, 219.442, 5.239),
        Measure(1626551362, 218.562, 5.639),
        Measure(1626551367, 221.682, 5.699),
        Measure(1626551372, 221.005, 5.18),
        Measure(1626551377, 217.802, 5.614),
        Measure(1626551382, 219.584, 5.385),
        Measure(1626551633, 219.111, 5.502),
        Measure(1626551729, 221.923, 5.411),
        Measure(1626551750, 218.024, 5.443),
        Measure(1626551755, 220.784, 5.18),
        Measure(1626551760, 217.849, 5.373),
        Measure(1626551765, 219.831, 5.362),
        Measure(1626551881, 221.5, 5.245),
        Measure(1626552004, 220.465, 5.685),
        Measure(1626552205, 221.847, 5.287),
        Measure(1626552281, 221.918, 5.602),
        Measure(1626552286, 219.383, 5.404),
    ]
    actual = controller.get_measures('5c7b5ffc-90e7-1b85-f041-0595c912c905', 5)
    assert actual.status_code == 200
    assert actual.body == [
        {'current': 5.432, 'power': 1198.141672, 'timestamp': '2021-07-17T19:48:16', 'voltage': 220.571},
        {'current': 5.555, 'power': 1224.45532, 'timestamp': '2021-07-17T19:48:22', 'voltage': 220.424},
        {'current': 5.512, 'power': 1209.3328, 'timestamp': '2021-07-17T19:48:28', 'voltage': 219.4},
        {'current': 5.628, 'power': 1232.13804, 'timestamp': '2021-07-17T19:48:34', 'voltage': 218.93},
        {'current': 5.579, 'power': 1222.676903, 'timestamp': '2021-07-17T19:48:40', 'voltage': 219.157},
        {'current': 5.676, 'power': 1253.84259, 'timestamp': '2021-07-17T19:48:46', 'voltage': 220.90249999999997},
        {'current': 5.449, 'power': 1187.66404, 'timestamp': '2021-07-17T19:48:52', 'voltage': 217.96},
        {'current': 5.239, 'power': 1149.656638, 'timestamp': '2021-07-17T19:48:58', 'voltage': 219.442},
        {'current': 5.639, 'power': 1232.4711180000002, 'timestamp': '2021-07-17T19:49:22', 'voltage': 218.562},
        {'current': 5.699, 'power': 1263.3657179999998, 'timestamp': '2021-07-17T19:49:28', 'voltage': 221.682},
        {'current': 5.18, 'power': 1144.8058999999998, 'timestamp': '2021-07-17T19:49:34', 'voltage': 221.005},
        {'current': 5.614, 'power': 1222.7404279999998, 'timestamp': '2021-07-17T19:49:40', 'voltage': 217.802},
        {'current': 5.385, 'power': 1182.45984, 'timestamp': '2021-07-17T19:49:46', 'voltage': 219.584}
    ]


def test_get_all_for_user_returns_ok_response_with_user_devices():
    controller = DevicesController(None)
    controller.device_repository.get_user_devices = lambda user_id: [
        Device('device_1', '5c7b5ffc-90e7-1b85-f041-0595c912c905'),
        Device('device_2', '5c7b5ffc-90e7-1b85-f041-0595c912c906'),
        Device('device_3', '5c7b5ffc-90e7-1b85-f041-0595c912c907'),
    ]
    actual = controller.get_all_for_user()
    assert actual.status_code == 200
    assert actual.body == [
        {'active': False, 'id': '5c7b5ffc-90e7-1b85-f041-0595c912c905', 'measures': [],
         'name': 'device_1', 'turned_on': False},
        {'active': False, 'id': '5c7b5ffc-90e7-1b85-f041-0595c912c906', 'measures': [],
         'name': 'device_2', 'turned_on': False},
        {'active': False, 'id': '5c7b5ffc-90e7-1b85-f041-0595c912c907', 'measures': [],
         'name': 'device_3', 'turned_on': False}
    ]
