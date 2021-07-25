from src.domain.exceptions.device_already_existent_exception import DeviceAlreadyExistentException
from src.domain.models.device import Device
from src.domain.repositories.device_repository import DeviceRepository


class DeviceCreator:

    def __init__(self, device_repository: DeviceRepository):
        self._device_repository = device_repository

    def create_device(self, device: Device, user_id: str) -> str:
        if self._device_repository.exists_for_user(device.id, user_id):
            raise DeviceAlreadyExistentException()
        self._device_repository.create(device, user_id)
        return device.id
