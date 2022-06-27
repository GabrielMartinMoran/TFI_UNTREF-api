from src.app.controllers.scheduler_controller import SchedulerController
from src.app.utils.http.request import Request
from src.domain.mappers.scheduling.tasks.task_mapper import TaskMapper


def test_set_scheduling_tasks_returns_ok_tasks_when_scheduling_tasks_are_updated_successfully():
    controller = SchedulerController(Request.from_body([
        {
            'action': 'TURN_DEVICE_ON',
            'moment': '2022-06-22T23:32:19.145344+00:00',
            'weekdays': [0, 2, 3]
        },
        {
            'action': 'TURN_DEVICE_OFF',
            'moment': '2022-06-30T14:25:19.145344+00:00'
        }
    ]))
    controller.device_repository.exists_for_user = lambda ble_id, user_id: True
    controller.device_scheduler_repository._has_scheduling_tasks = lambda device_id: False
    controller.device_scheduler_repository._create_scheduling_tasks = lambda device, tasks: None
    actual = controller.set_scheduling_tasks('5c7b5ffc-90e7-1b85-f041-0595c912c905')
    assert actual.status_code == 200


def test_set_scheduling_tasks_returns_error_response_when_user_does_not_have_provided_device():
    controller = SchedulerController(Request.from_body([]))
    controller.device_repository.exists_for_user = lambda ble_id, user_id: False
    actual = controller.set_scheduling_tasks('5c7b5ffc-90e7-1b85-f041-0595c912c905')
    assert actual.status_code == 400
    assert actual.body['message'] == 'Provided device_id does not match any of the user devices'


def test_set_scheduling_tasks_returns_error_response_when_a_task_is_not_valid():
    controller = SchedulerController(Request.from_body([
        {
            'action': 'TURN_DEVICE_ON'
        }
    ]))
    actual = controller.set_scheduling_tasks('5c7b5ffc-90e7-1b85-f041-0595c912c905')
    assert actual.status_code == 400
    assert actual.body['message'] == 'Task.moment must not be None'


def test_get_scheduling_tasks_returns_error_response_when_user_does_not_have_provided_device():
    controller = SchedulerController(None)
    controller.device_repository.exists_for_user = lambda ble_id, user_id: False
    actual = controller.get_scheduling_tasks('5c7b5ffc-90e7-1b85-f041-0595c912c905')
    assert actual.status_code == 400
    assert actual.body['message'] == 'Provided device_id does not match any of the user devices'


def test_get_scheduling_tasks_returns_a_list_of_scheduled_tasks():
    controller = SchedulerController(None)
    device_tasks = [
        {
            'action': 'TURN_DEVICE_ON',
            'moment': '2022-06-22T23:32:19.145344+00:00',
            'weekdays': [0, 2, 3]
        },
        {
            'action': 'TURN_DEVICE_OFF',
            'moment': '2022-06-30T14:25:19.145344+00:00'
        }
    ]
    controller.device_repository.exists_for_user = lambda ble_id, user_id: True
    controller.device_scheduler_repository.get_scheduling_tasks = lambda device_id: TaskMapper.map_all(device_tasks)
    actual = controller.get_scheduling_tasks('5c7b5ffc-90e7-1b85-f041-0595c912c905')
    assert actual.status_code == 200
    assert actual.body == device_tasks
