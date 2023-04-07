from src.common import dates
from src.domain.exceptions.unregistered_device_exception import UnregisteredDeviceException
from src.domain.repositories.device_repository import DeviceRepository


class DeviceStateRetriever:

    def __init__(self, device_repository: DeviceRepository):
        self._device_repository = device_repository

    def get(self, device_id: str, user_id: str) -> bool:
        if not self._device_repository.exists_for_user(device_id, user_id):
            raise UnregisteredDeviceException()
        return self._device_repository.get_state(device_id, user_id)
