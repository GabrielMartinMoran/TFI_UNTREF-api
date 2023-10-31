from src.domain.exceptions.unregistered_device_exception import UnregisteredDeviceException
from src.app.utils.auth.device_token import DeviceToken
from src.domain.repositories.device_repository import DeviceRepository


class DeviceTokenGenerator:

    def __init__(self, device_repository: DeviceRepository) -> None:
        self._device_repository = device_repository

    def generate(self, user_id: str, device_id: str) -> DeviceToken:
        if not self._device_repository.exists_for_user(device_id, user_id):
            raise UnregisteredDeviceException()
        return DeviceToken(user_id=user_id, device_id=device_id)
