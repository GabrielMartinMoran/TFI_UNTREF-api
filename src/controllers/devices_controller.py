from src.exceptions.device_already_existent_exception import DeviceAlreadyExistentException
from src.exceptions.unregistered_device_exception import UnregisteredDeviceException
from src.repositories.measure_repository import MeasureRepository
from src.models.measure import Measure
from src.services.devices.device_creator import DeviceCreator
from src.services.devices.device_measure_aggregator import DeviceMeasureAggregator
from src.services.devices.device_measure_summarizer import DeviceMeasureSummarizer
from src.services.devices.devices_obtainer import DevicesRetriever
from src.utils.http.response import Response
from src.utils.http.route import route
from src.utils.logger import Logger
from src.controllers.base_controller import BaseController
from src.utils.http import http_methods
from src.utils.ble_id_generator import BleIdGenerator
from src.models.device import Device
from src.repositories.device_repository import DeviceRepository


class DevicesController(BaseController):

    def __init__(self) -> None:
        super().__init__()
        self.device_repository = DeviceRepository()
        self.measure_repository = MeasureRepository()

    @route(http_methods.GET)
    def generate_ble_id(self) -> Response:
        return self.ok({'ble_id': BleIdGenerator.generate_ble_id()})

    @route(http_methods.POST, auth_required=True)
    def create(self) -> Response:
        device = Device.from_dict(self.get_json_body())
        if not device.is_valid():
            return self.validation_error(device.validation_errors)
        device_creator = DeviceCreator(self.device_repository)
        try:
            device_id = device_creator.create_device(device, self.get_authenticated_user_id())
        except DeviceAlreadyExistentException:
            return self.error('There is another device with the same ble_id for logged user')
        except Exception as ex:
            Logger.get_logger(__file__).error(ex)
            return self.error('An error has occurred while creating the device')
        return self.created_ok(device_id)

    @route(http_methods.POST, auth_required=True)
    def add_measure(self, ble_id: str) -> Response:
        measure = Measure.from_dict(self.get_json_body())
        if not measure.is_valid():
            return self.validation_error(measure.validation_errors)
        device_measure_aggregator = DeviceMeasureAggregator(self.device_repository, self.measure_repository)
        try:
            device_measure_aggregator.add_measure_to_device(ble_id, self.get_authenticated_user_id(), measure)
        except UnregisteredDeviceException:
            return self.error('Device identifier is not valid for logged user')
        except Exception as ex:
            Logger.get_logger(__file__).error(ex)
            return self.error('An error has ocurred while creating the measure')
        return self.created_ok()

    @route(http_methods.GET, auth_required=True)
    def get_measures(self, ble_id: str, time_interval: int) -> Response:
        summarizer = DeviceMeasureSummarizer(self.device_repository, self.measure_repository)
        try:
            measures = summarizer.get_summarized_measures(ble_id, self.get_authenticated_user_id(), time_interval)
        except UnregisteredDeviceException:
            return self.error('Device identifier is not valid for logged user')
        return self.ok([x.to_dict() for x in measures])

    @route(http_methods.GET, auth_required=True)
    def get_all(self) -> Response:
        devices_retriever = DevicesRetriever(self.device_repository)
        try:
            devices = devices_retriever.get_user_devices(self.get_authenticated_user_id())
        except Exception:
            return self.error('An error has occurred while trying to obtain logged user devices')
        return self.ok([device.to_dict() for device in devices])
