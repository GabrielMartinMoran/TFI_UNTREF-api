from src.exceptions.device_already_existent_exception import DeviceAlreadyExistentException
from src.models.device import Device
from src.repositories.device_repository import DeviceRepository


class DeviceCreator:

    def __init__(self, device_repository: DeviceRepository):
        self._device_repository = device_repository

    def create_device(self, device: Device, user_id: str) -> str:
        if self._device_repository.ble_id_exists_for_user(device.ble_id, user_id):
            raise DeviceAlreadyExistentException()
        return self._device_repository.insert(device, user_id)
