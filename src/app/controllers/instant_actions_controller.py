from typing import Optional

from src.app.utils.auth.permission_level import PermissionLevel
from src.app.utils.auth.token import Token
from src.app.utils.http.request import Request
from src.domain.exceptions.device_not_found_exception import DeviceNotFoundException
from src.domain.models.scheduling.tasks.task_action import TaskAction
from src.app.utils.http.response import Response
from src.app.utils.http.route import route
from src.app.utils.logging.logger import Logger
from src.app.controllers.base_controller import BaseController
from src.app.utils.http import http_methods
from src.domain.services.instant_actions.instant_action_puller import InstantActionPuller
from src.domain.services.instant_actions.instant_action_pusher import InstantActionPusher
from src.infrastructure.repositories.device_pg_repository import DevicePGRepository
from src.infrastructure.repositories.instant_action_pg_repository import InstantActionPGRepository


class InstantActionsController(BaseController):

    def __init__(self, request: Request, token: Optional[Token] = None) -> None:
        super().__init__(request, token)
        self.device_repository = DevicePGRepository()
        self.instant_action_repository = InstantActionPGRepository()

    @route(http_methods.POST, alias='action')
    def push_instant_action(self, device_id: str) -> Response:
        try:
            action = TaskAction(self.get_json_body().get('action'))
            pusher = InstantActionPusher(self.device_repository, self.instant_action_repository)
            pusher.push(device_id, self.get_authenticated_user_id(), action)
            return Response.success()
        except ValueError as e:
            Logger.error(e)
            return Response.bad_request('Provided action is not a valid TaskAction')
        except DeviceNotFoundException as e:
            Logger.error(e)
            return Response.bad_request('Provided device_id does not match any of the user devices')
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred when pushing the instant action')

    @route(http_methods.GET, alias='action', min_permission_level=PermissionLevel.DEVICE)
    def pull_instant_action(self, device_id: str) -> Response:
        try:
            self._validate_device_permission(device_id)
            puller = InstantActionPuller(self.device_repository, self.instant_action_repository)
            action = puller.pull(device_id, self.get_authenticated_user_id())
            return Response.success({'action': action.value if action is not None else None})
        except DeviceNotFoundException as e:
            Logger.error(e)
            return Response.bad_request('Provided device_id does not match any of the user devices')
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred when pushing the instant action')
