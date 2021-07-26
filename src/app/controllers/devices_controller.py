from src.app.utils.auth_info import AuthInfo
from src.app.utils.http.request import Request
from src.domain.exceptions.device_already_existent_exception import DeviceAlreadyExistentException
from src.domain.exceptions.unregistered_device_exception import UnregisteredDeviceException
from src.domain.models.device import Device
from src.domain.models.measure import Measure
from src.domain.services.devices.device_creator import DeviceCreator
from src.domain.services.devices.device_measure_aggregator import DeviceMeasureAggregator
from src.domain.services.devices.device_measure_summarizer import DeviceMeasureSummarizer
from src.domain.services.devices.devices_obtainer import DevicesRetriever
from src.app.utils.http.response import Response
from src.app.utils.http.route import route
from src.app.utils.logging.logger import Logger
from src.app.controllers.base_controller import BaseController
from src.app.utils.http import http_methods
from src.infrastructure.repositories.device_pg_repository import DevicePGRepository
from src.infrastructure.repositories.measure_pg_repository import MeasurePGRepository


class DevicesController(BaseController):

    def __init__(self, request: Request, auth_info: AuthInfo = None) -> None:
        super().__init__(request, auth_info)
        self.device_repository = DevicePGRepository()
        self.measure_repository = MeasurePGRepository()

    """
    @route(http_methods.GET)
    def generate_ble_id(self) -> Response:
        return self.ok({'device_id': BleIdGenerator.generate_ble_id()})
    """

    @route(http_methods.POST, auth_required=True)
    def create(self) -> Response:
        device = Device.from_dict(self.get_json_body(), set_id=False)
        if not device.is_valid():
            return Response.bad_request(validation_errors=device.validation_errors)
        device_creator = DeviceCreator(self.device_repository)
        try:
            device_id = device_creator.create_device(device, self.get_authenticated_user_id())
        except DeviceAlreadyExistentException:
            return Response.conflict('There is another device with the same device_id for logged user')
        except Exception as e:
            print(e)
            Logger.get_logger(__file__).error(e)
            return Response.server_error('An error has occurred while creating the device')
        return Response.created_successfully(device_id)

    @route(http_methods.POST, auth_required=True)
    def add_measure(self, device_id: str) -> Response:
        measure = Measure.from_dict(self.get_json_body())
        if not measure.is_valid():
            return Response.bad_request(validation_errors=measure.validation_errors)
        device_measure_aggregator = DeviceMeasureAggregator(self.device_repository, self.measure_repository)
        try:
            device_measure_aggregator.add_measure_to_device(device_id, self.get_authenticated_user_id(), measure)
        except UnregisteredDeviceException:
            return Response.bad_request(message='Device identifier is not valid for logged user')
        except Exception as e:
            print(e)
            Logger.get_logger(__file__).error(e)
            return Response.server_error('An error has ocurred while creating the measure')
        return Response.created_successfully()

    @route(http_methods.GET, auth_required=True)
    def get_measures(self, device_id: str, time_interval: int) -> Response:
        summarizer = DeviceMeasureSummarizer(self.device_repository, self.measure_repository)
        try:
            measures = summarizer.get_summarized_measures(device_id, self.get_authenticated_user_id(), time_interval)
        except UnregisteredDeviceException:
            return Response.bad_request(message='Device identifier is not valid for logged user')
        except Exception as e:
            print(e)
            return Response.server_error('An error has occurred while trying to obtain device measures')
        return Response.success([x.to_dict() for x in measures])

    @route(http_methods.GET, alias='get_all', auth_required=True)
    def get_all_for_user(self) -> Response:
        devices_retriever = DevicesRetriever(self.device_repository)
        try:
            devices = devices_retriever.get_user_devices(self.get_authenticated_user_id())
        except Exception as e:
            print(e)
            return Response.server_error('An error has occurred while trying to obtain logged user devices')
        return Response.success([device.to_dict() for device in devices])
