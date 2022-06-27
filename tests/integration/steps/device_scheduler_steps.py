import random
from typing import List

from pytest_bdd import given, then, when, parsers

from src.app.controllers.scheduler_controller import SchedulerController
from src.app.utils.http.request import Request
from src.domain.models.scheduling.tasks.task import Task
from src.domain.serializers.scheduling.tasks.task_serializer import TaskSerializer
from src.infrastructure.repositories.device_scheduler_pg_repository import DeviceSchedulerPGRepository
from tests.integration.utils import shared_variables
from tests.model_stubs.scheduling.tasks.daily_task_stub import DailyTaskStub
from tests.model_stubs.scheduling.tasks.task_stub import TaskStub

last_device_scheduling_tasks: List[Task] = []


@given(parsers.cfparse('device with id \'{device_id}\' has scheduling tasks'))
def device_has_scheduling_tasks(device_id: str):
    device_scheduling_repository = DeviceSchedulerPGRepository()
    tasks = []
    for x in range(5):
        tasks.append(TaskStub())
        tasks.append(DailyTaskStub())
    device_scheduling_repository.set_scheduling_tasks(device_id, tasks)
    global last_device_scheduling_tasks
    last_device_scheduling_tasks = tasks


@when(parsers.cfparse('user tries to set some valid scheduling task to the device with id \'{device_id}\''))
def try_set_valid_scheduling_tasks(device_id: str):
    tasks = []
    # Add some of each type of task
    for x in range(random.randint(2, 5)):
        tasks.append(TaskStub())
        tasks.append(DailyTaskStub())
    controller = SchedulerController(request=Request.from_body(TaskSerializer.serialize_all(tasks)),
                                     auth_info=shared_variables.logged_auth_info)
    shared_variables.last_response = controller.set_scheduling_tasks(device_id)


@when(parsers.cfparse('user tries to get scheduling tasks for device with id \'{device_id}\''))
def try_get_valid_tasks(device_id: str):
    controller = SchedulerController(request=None, auth_info=shared_variables.logged_auth_info)
    shared_variables.last_response = controller.get_scheduling_tasks(device_id)


@then('device has those scheduling tasks configured successfully')
def scheduling_tasks_set_successfully():
    assert shared_variables.last_response.status_code == 200


@then('scheduling tasks are returned successfully')
def scheduling_tasks_get_successfully():
    assert shared_variables.last_response.status_code == 200
    assert shared_variables.last_response.body == TaskSerializer.serialize_all(last_device_scheduling_tasks)
