from abc import ABC, abstractmethod
from typing import List

from src.domain.models.device import Device


class DeviceRepository(ABC):

    @abstractmethod
    def create(self, device: Device, user_id: str) -> None: pass

    @abstractmethod
    def exists_for_user(self, device_id: str, user_id: str) -> bool: pass

    @abstractmethod
    def get_user_devices(self, user_id: str) -> List[Device]: pass
