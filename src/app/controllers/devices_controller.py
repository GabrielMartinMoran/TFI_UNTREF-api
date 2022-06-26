from src.app.utils.auth_info import AuthInfo
from src.app.utils.http.request import Request
from src.domain.exceptions.device_already_existent_exception import DeviceAlreadyExistentException
from src.domain.exceptions.device_not_found_exception import DeviceNotFoundException
from src.domain.exceptions.model_validation_exception import ModelValidationException
from src.domain.exceptions.unregistered_device_exception import UnregisteredDeviceException
from src.domain.mappers.device_mapper import DeviceMapper
from src.domain.mappers.measure_mapper import MeasureMapper
from src.domain.mappers.scheduling.tasks.task_mapper import TaskMapper
from src.domain.serializers.device_serializer import DeviceSerializer
from src.domain.serializers.measure_serializer import MeasureSerializer
from src.domain.serializers.scheduling.tasks.task_serializer import TaskSerializer
from src.domain.services.devices.device_creator import DeviceCreator
from src.domain.services.devices.device_measure_aggregator import DeviceMeasureAggregator
from src.domain.services.devices.device_measure_summarizer import DeviceMeasureSummarizer
from src.domain.services.devices.device_scheduler_retriever import DeviceSchedulerRetriever
from src.domain.services.devices.device_scheduler_updater import DeviceSchedulerUpdater
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

    @route(http_methods.POST)
    def create(self) -> Response:
        try:
            device = DeviceMapper.map(self.get_json_body(), set_id=False)
            device_creator = DeviceCreator(self.device_repository)
            device_id = device_creator.create_device(device, self.get_authenticated_user_id())
            return Response.created_successfully(device_id)
        except ModelValidationException as e:
            return Response.bad_request(validation_errors=e.validation_errors)
        except DeviceAlreadyExistentException:
            return Response.conflict('There is another device with the same device_id for logged user')
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred while creating the device')

    @route(http_methods.POST)
    def add_measure(self, device_id: str) -> Response:
        try:
            measure = MeasureMapper.map(self.get_json_body())
            device_measure_aggregator = DeviceMeasureAggregator(self.device_repository, self.measure_repository)
            device_measure_aggregator.add_measure_to_device(device_id, self.get_authenticated_user_id(), measure)
            return Response.created_successfully()
        except ModelValidationException as e:
            return Response.bad_request(validation_errors=e.validation_errors)
        except UnregisteredDeviceException:
            return Response.bad_request(message='Device identifier is not valid for logged user')
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred while creating the measure')

    @route(http_methods.GET)
    def get_measures(self, device_id: str, time_interval: int) -> Response:
        try:
            summarizer = DeviceMeasureSummarizer(self.device_repository, self.measure_repository)
            measures = summarizer.get_summarized_measures(device_id, self.get_authenticated_user_id(), time_interval)
            return Response.success(MeasureSerializer.serialize_all(measures))
        except UnregisteredDeviceException:
            return Response.bad_request(message='Device identifier is not valid for logged user')
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred while trying to obtain device measures')

    @route(http_methods.GET, alias='get_all')
    def get_all_for_user(self) -> Response:
        try:
            devices_retriever = DevicesRetriever(self.device_repository)
            devices = devices_retriever.get_user_devices(self.get_authenticated_user_id())
            return Response.success(DeviceSerializer.serialize_all(devices))
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred while trying to obtain logged user devices')

    @route(http_methods.POST)
    def set_scheduling_tasks(self, device_id: str) -> Response:
        try:
            tasks = TaskMapper.map_all(self.get_json_body())
            updater = DeviceSchedulerUpdater(self.device_repository)
            updater.set_scheduling_tasks(device_id, self.get_authenticated_user_id(), tasks)
            return Response.success()
        except ModelValidationException as e:
            Logger.error(e)
            return Response.bad_request(validation_errors=e.validation_errors)
        except DeviceNotFoundException as e:
            Logger.error(e)
            return Response.bad_request('Provided device_id does not match any of the user devices')
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred while updating device scheduling')

    @route(http_methods.GET)
    def get_scheduling_tasks(self, device_id: str) -> Response:
        try:
            retriever = DeviceSchedulerRetriever(self.device_repository)
            tasks = retriever.get_scheduling_tasks(device_id, self.get_authenticated_user_id())
            return Response.success(TaskSerializer.serialize_all(tasks))
        except ModelValidationException as e:
            Logger.error(e)
            return Response.bad_request(validation_errors=e.validation_errors)
        except DeviceNotFoundException as e:
            Logger.error(e)
            return Response.bad_request('Provided device_id does not match any of the user devices')
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred while getting device scheduling')
