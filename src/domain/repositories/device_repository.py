from abc import ABC, abstractmethod
from typing import List

from src.domain.models.device import Device
from src.domain.models.scheduling.tasks.task import Task


class DeviceRepository(ABC):

    @abstractmethod
    def create(self, device: Device, user_id: str) -> None: pass

    @abstractmethod
    def exists_for_user(self, device_id: str, user_id: str) -> bool: pass

    @abstractmethod
    def get_user_devices(self, user_id: str) -> List[Device]: pass

    @abstractmethod
    def set_scheduling_tasks(self, device_id: str, tasks: List[Task]) -> None: pass

    @abstractmethod
    def get_scheduling_tasks(self, device_id: str) -> List[Task]: pass
