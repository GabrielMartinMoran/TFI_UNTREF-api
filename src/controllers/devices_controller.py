from src.repositories.measure_repository import MeasureRepository
from src.models.measure import Measure
from src.utils.logger import Logger
from src.controllers.base_controller import BaseController, http_method
from src.utils import http_methods
from src.utils.ble_id_generator import BLEIdGenerator
from src.models.device import Device
from src.repositories.device_repository import DeviceRepository


class DevicesController(BaseController):

    def __init__(self):
        super().__init__()
        self.device_repository = DeviceRepository()
        self.measure_repository = MeasureRepository()

    @http_method(http_methods.GET)
    def generate_ble_id(self) -> dict:
        return self.ok_success({'bleId': BLEIdGenerator.generate_ble_id()})

    @http_method(http_methods.POST, auth_required=True)
    def create(self) -> dict:
        device = Device.from_dict(self.get_json_body())
        user_id = self.get_authenticated_user_id()
        if not device.is_valid():
            return self.validation_error(device.validation_errors)
        if self.device_repository.ble_id_exists_for_user(device.ble_id, user_id):
            return self.error('Ya existe un dispositivo con el mismo bleId')
        try:
            device.device_id = self.device_repository.insert(device, user_id)
        except Exception as ex:
            Logger.get_logger(__file__).error(ex)
            return self.error('An error has ocurred while creating the device')
        return self.created_ok(device.device_id)

    @http_method(http_methods.POST, auth_required=True)
    def add_measure(self, ble_id: str) -> dict:
        measure = Measure.from_dict(self.get_json_body())
        user_id = self.get_authenticated_user_id()
        if not measure.is_valid():
            return self.validation_error(measure.validation_errors)
        try:
            self.measure_repository.insert(measure, ble_id, user_id)
        except Exception as ex:
            Logger.get_logger(__file__).error(ex)
            return self.error('An error has ocurred while creating the measure')
        return self.ok_success()
