from src.exceptions.unregistered_device_exception import UnregisteredDeviceException
from src.models.measure import Measure
from src.repositories.device_repository import DeviceRepository
from src.repositories.measure_repository import MeasureRepository


class DeviceMeasureAggregator:

    def __init__(self, device_repository: DeviceRepository, measure_repository: MeasureRepository):
        self._device_repository = device_repository
        self._measure_repository = measure_repository

    def add_measure_to_device(self, ble_id: str, user_id: str, measure: Measure):
        if not self._device_repository.ble_id_exists_for_user(ble_id, user_id):
            raise UnregisteredDeviceException()
        self._measure_repository.insert(measure, ble_id, user_id)
