from typing import List, Optional

from src.domain.exceptions.device_not_found_exception import DeviceNotFoundException
from src.domain.models.scheduling.scheduler_action import SchedulerAction
from src.domain.models.scheduling.scheduling_stack import SchedulingStack
from src.domain.models.scheduling.tasks.task import Task
from src.domain.repositories.device_repository import DeviceRepository
from src.domain.repositories.device_scheduler_repository import DeviceSchedulerRepository


class DeviceSchedulerRetriever:

    def __init__(self, device_repository: DeviceRepository,
                 device_scheduler_repository: DeviceSchedulerRepository) -> None:
        self._device_repository = device_repository
        self._device_scheduler_repository = device_scheduler_repository

    def get_scheduling_tasks(self, device_id: str, user_id: str) -> List[Task]:
        if not self._device_repository.exists_for_user(device_id, user_id):
            raise DeviceNotFoundException()
        return self._device_scheduler_repository.get_scheduling_tasks(device_id)

    def get_next_scheduling_action(self, device_id: str, user_id: str) -> Optional[SchedulerAction]:
        scheduling_tasks = self.get_scheduling_tasks(device_id, user_id)
        scheduling_stack = SchedulingStack(scheduling_tasks)
        return scheduling_stack.get_next_action()
