import random
from datetime import timedelta
from typing import List

from pytest_bdd import given, then, when, parsers

from src.app.controllers.devices_controller import DevicesController
from src.app.utils.http.request import Request
from src.common import dates
from src.domain.models.device import Device
from src.domain.models.scheduling.tasks.task import Task
from src.domain.models.user import User
from src.domain.serializers.task_serializer import TaskSerializer
from src.infrastructure.repositories.device_pg_repository import DevicePGRepository
from src.infrastructure.repositories.measure_pg_repository import MeasurePGRepository
from tests.integration.utils import shared_variables
from tests.model_stubs.measure_stub import MeasureStub
from tests.model_stubs.scheduling.tasks.daily_task_stub import DailyTaskStub
from tests.model_stubs.scheduling.tasks.task_stub import TaskStub

last_device_scheduling_tasks: List[Task] = []


@given(parsers.cfparse('device with id \'{device_id}\' exists for logged user'))
def device_exists_for_logged_user(device_id: str):
    device_repository = DevicePGRepository()
    device = Device(name=device_id, device_id=device_id)
    user_id = User.email_to_id(shared_variables.logged_auth_info.user_email)
    if not device_repository.exists_for_user(device_id, user_id):
        device_repository.create(device, user_id)


@given(parsers.cfparse('device with id \'{device_id}\' has recent measures'))
def device_has_recent_measures(device_id: str):
    measure_repository = MeasurePGRepository()
    minutes_interval = 0.0
    while minutes_interval <= 10:  # Until 10 minutes
        measure = MeasureStub(timestamp=dates.now() - timedelta(minutes=minutes_interval))
        measure_repository.create(measure, device_id)
        minutes_interval += 0.5


@given(parsers.cfparse('device with id \'{device_id}\' has scheduling tasks'))
def device_has_scheduling_tasks(device_id: str):
    device_repository = DevicePGRepository()
    tasks = []
    for x in range(5):
        tasks.append(TaskStub())
        tasks.append(DailyTaskStub())
    device_repository.set_scheduling_tasks(device_id, tasks)
    global last_device_scheduling_tasks
    last_device_scheduling_tasks = tasks


@when(parsers.cfparse('user tries to create device with name \'{device_name}\''))
def try_user_login(device_name: str):
    controller = DevicesController(request=Request.from_body({
        'name': device_name
    }), auth_info=shared_variables.logged_auth_info)
    shared_variables.last_response = controller.create()


@when(parsers.cfparse('user tries to add a measure for device with id \'{device_id}\''))
def try_add_valid_measure(device_id: str):
    controller = DevicesController(request=Request.from_body(MeasureStub().to_dict()),
                                   auth_info=shared_variables.logged_auth_info)
    shared_variables.last_response = controller.add_measure(device_id)


@when(parsers.cfparse('user tries to add an invalid measure for device with id \'{device_id}\''))
def try_add_invalid_measure(device_id: str):
    measure_dict = {
        **MeasureStub().to_dict(), **{
            'voltage': -200.0,
            'current': -5.0
        }
    }
    controller = DevicesController(request=Request.from_body(measure_dict), auth_info=shared_variables.logged_auth_info)
    shared_variables.last_response = controller.add_measure(device_id)


@when(parsers.cfparse('user tries to get measures for device with id \'{device_id}\''))
def try_get_measures_for_device(device_id: str):
    controller = DevicesController(request=None, auth_info=shared_variables.logged_auth_info)
    minutes_interval = 10
    shared_variables.last_response = controller.get_measures(device_id, minutes_interval)


@when(parsers.cfparse('user tries to set some valid scheduling task to the device with id \'{device_id}\''))
def try_set_valid_scheduling_tasks(device_id: str):
    tasks = []
    # Add some of each type of task
    for x in range(random.randint(2, 5)):
        tasks.append(TaskStub())
        tasks.append(DailyTaskStub())
    controller = DevicesController(request=Request.from_body(TaskSerializer.serialize_tasks(tasks)),
                                   auth_info=shared_variables.logged_auth_info)
    shared_variables.last_response = controller.set_scheduling_tasks(device_id)


@when(parsers.cfparse('user tries to get scheduling tasks for device with id \'{device_id}\''))
def try_get_valid_tasks(device_id: str):
    controller = DevicesController(request=None, auth_info=shared_variables.logged_auth_info)
    shared_variables.last_response = controller.get_scheduling_tasks(device_id)


@then('device is created successfully')
def device_created_successfully():
    assert shared_variables.last_response.status_code == 201


@then('measure is added successfully')
def measure_added_successfully():
    assert shared_variables.last_response.status_code == 201


@then('measure addition fails')
def measure_addition_fails():
    assert shared_variables.last_response.status_code == 400


@then('summarized measures are returned successfully')
def summarized_measures_returned_successfully():
    assert shared_variables.last_response.status_code == 200
    assert len(shared_variables.last_response.body) > 0
    for measure in shared_variables.last_response.body:
        assert 'current' in measure
        assert 'voltage' in measure
        assert 'power' in measure
        assert 'timestamp' in measure


@then('device has those scheduling tasks configured successfully')
def scheduling_tasks_set_successfully():
    assert shared_variables.last_response.status_code == 200


@then('scheduling tasks are returned successfully')
def scheduling_tasks_get_successfully():
    assert shared_variables.last_response.status_code == 200
    assert shared_variables.last_response.body == TaskSerializer.serialize_tasks(last_device_scheduling_tasks)
