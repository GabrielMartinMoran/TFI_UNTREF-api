from src.common import dates
from src.domain.exceptions.unregistered_device_exception import UnregisteredDeviceException
from src.domain.repositories.device_repository import DeviceRepository


class DeviceStateModifier:

    def __init__(self, device_repository: DeviceRepository):
        self._device_repository = device_repository

    def update(self, device_id: str, user_id: str, turned_on: bool) -> None:
        if not self._device_repository.exists_for_user(device_id, user_id):
            raise UnregisteredDeviceException()
        last_status_update = dates.now()
        self._device_repository.update_state(device_id, user_id, turned_on, last_status_update)
