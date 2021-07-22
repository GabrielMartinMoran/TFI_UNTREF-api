from typing import List

from src.models.device import Device
from src.repositories.device_repository import DeviceRepository


class DevicesRetriever:

    def __init__(self, device_repository: DeviceRepository):
        self._device_repository = device_repository

    def get_user_devices(self, user_id: str) -> List[Device]:
        return self._device_repository.get_user_devices(user_id)
