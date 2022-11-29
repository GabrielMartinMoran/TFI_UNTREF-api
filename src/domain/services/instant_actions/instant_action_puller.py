from datetime import timedelta
from typing import Optional

from src.common import dates
from src.config import INSTANT_ACTIONS_LIFETIME
from src.domain.exceptions.device_not_found_exception import DeviceNotFoundException
from src.domain.models.scheduling.tasks.task_action import TaskAction
from src.domain.repositories.device_repository import DeviceRepository
from src.domain.repositories.instant_action_repository import InstantActionRepository


class InstantActionPuller:

    def __init__(self, device_repository: DeviceRepository, instant_action_repository: InstantActionRepository) -> None:
        self._device_repository = device_repository
        self._instant_action_repository = instant_action_repository

    def pull(self, device_id: str, user_id: str) -> Optional[TaskAction]:
        if not self._device_repository.exists_for_user(device_id, user_id):
            raise DeviceNotFoundException()
        pull_until = dates.now() - timedelta(seconds=INSTANT_ACTIONS_LIFETIME)
        action = self._instant_action_repository.pull(device_id, pull_until)
        self._instant_action_repository.clean_for(device_id)
        return action
