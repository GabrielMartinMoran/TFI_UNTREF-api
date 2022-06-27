from typing import List

from src.domain.exceptions.device_not_found_exception import DeviceNotFoundException
from src.domain.models.scheduling.tasks.task import Task
from src.domain.repositories.device_repository import DeviceRepository
from src.domain.repositories.device_scheduler_repository import DeviceSchedulerRepository


class DeviceSchedulerUpdater:

    def __init__(self, device_repository: DeviceRepository,
                 device_scheduler_repository: DeviceSchedulerRepository) -> None:
        self._device_repository = device_repository
        self._device_scheduler_repository = device_scheduler_repository

    def set_scheduling_tasks(self, device_id: str, user_id: int, tasks: List[Task]) -> None:
        if not self._device_repository.exists_for_user(device_id, user_id):
            raise DeviceNotFoundException()
        self._device_scheduler_repository.set_scheduling_tasks(device_id, tasks)
