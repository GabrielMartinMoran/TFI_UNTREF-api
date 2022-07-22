from src.domain.exceptions.unregistered_device_exception import UnregisteredDeviceException
from src.domain.models.measure import Measure
from src.domain.repositories.device_repository import DeviceRepository
from src.domain.repositories.measure_repository import MeasureRepository


class DeviceMeasureAggregator:

    def __init__(self, device_repository: DeviceRepository, measure_repository: MeasureRepository):
        self._device_repository = device_repository
        self._measure_repository = measure_repository

    def add_measure_to_device(self, device_id: str, user_id: str, measure: Measure):
        if not self._device_repository.exists_for_user(device_id, user_id):
            raise UnregisteredDeviceException()
        self._measure_repository.create(measure, device_id)
