from src.domain.exceptions.device_not_found_exception import DeviceNotFoundException
from src.domain.models.scheduling.tasks.task_action import TaskAction
from src.domain.repositories.device_repository import DeviceRepository
from src.domain.repositories.instant_action_repository import InstantActionRepository


class InstantActionPusher:

    def __init__(self, device_repository: DeviceRepository, instant_action_repository: InstantActionRepository) -> None:
        self._device_repository = device_repository
        self._instant_action_repository = instant_action_repository

    def push(self, device_id: str, user_id: str, action: TaskAction) -> None:
        if not self._device_repository.exists_for_user(device_id, user_id):
            raise DeviceNotFoundException()
        self._instant_action_repository.clean_for(device_id)
        self._instant_action_repository.push(device_id, action)
