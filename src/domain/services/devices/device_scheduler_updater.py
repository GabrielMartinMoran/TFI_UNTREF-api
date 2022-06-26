from typing import List

from src.domain.exceptions.device_not_found_exception import DeviceNotFoundException
from src.domain.models.scheduling.tasks.task import Task
from src.domain.repositories.device_repository import DeviceRepository


class DeviceSchedulerUpdater:

    def __init__(self, device_repository: DeviceRepository):
        self._device_repository = device_repository

    def set_scheduling_tasks(self, device_id: str, user_id: int, tasks: List[Task]) -> None:
        if not self._device_repository.exists_for_user(device_id, user_id):
            raise DeviceNotFoundException()
        self._device_repository.set_scheduling_tasks(device_id, tasks)
