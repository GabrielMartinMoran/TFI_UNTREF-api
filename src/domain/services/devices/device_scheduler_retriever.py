from typing import List

from src.domain.exceptions.device_not_found_exception import DeviceNotFoundException
from src.domain.models.scheduling.tasks.task import Task
from src.domain.repositories.device_repository import DeviceRepository


class DeviceSchedulerRetriever:

    def __init__(self, device_repository: DeviceRepository):
        self._device_repository = device_repository

    def get_scheduling_tasks(self, device_id: str, user_id: int) -> List[Task]:
        if not self._device_repository.exists_for_user(device_id, user_id):
            raise DeviceNotFoundException()
        return self._device_repository.get_scheduling_tasks(device_id)
