from typing import Optional

from pymodelio.exceptions import ModelValidationException

from src.app.controllers.base_controller import BaseController
from src.app.utils.auth.permission_level import PermissionLevel
from src.app.utils.auth.token import Token
from src.app.utils.auth.user_token import UserToken
from src.app.utils.http.request import Request
from src.app.utils.logging.logger import Logger
from src.domain.exceptions.email_already_registered_exception import EmailAlreadyRegisteredException
from src.domain.exceptions.invalid_login_exception import InvalidLoginException
from src.domain.exceptions.invalid_user_exception import InvalidUserException
from src.domain.exceptions.unregistered_device_exception import UnregisteredDeviceException
from src.domain.mappers.user_mapper import UserMapper
from src.domain.serializers.user_serializer import UserSerializer
from src.domain.services.auth.device_token_generator import DeviceTokenGenerator
from src.domain.services.auth.user_logger import UserLogger
from src.domain.services.auth.user_obtainer import UserObtainer
from src.domain.services.auth.user_registerer import UserRegisterer
from src.app.utils.http import http_methods
from src.app.utils.http.response import Response
from src.app.utils.http.route import route
from src.infrastructure.repositories.device_pg_repository import DevicePGRepository
from src.infrastructure.repositories.user_pg_repository import UserPGRepository


class AuthController(BaseController):

    def __init__(self, request: Request, token: Optional[Token] = None) -> None:
        super().__init__(request, token)
        self.user_repository = UserPGRepository()
        self.device_repository = DevicePGRepository()

    @route(http_methods.POST, min_permission_level=PermissionLevel.PUBLIC)
    def register(self) -> Response:
        try:
            user = UserMapper.map(self.get_json_body())
            user_registerer = UserRegisterer(self.user_repository)
            user_registerer.register_user(user)
            return Response.created_successfully()
        except ModelValidationException as e:
            return Response.bad_request(message=str(e))
        except EmailAlreadyRegisteredException:
            return Response.conflict('User with same email already exists')
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred while creating user')

    @route(http_methods.POST, min_permission_level=PermissionLevel.PUBLIC)
    def login(self) -> Response:
        body = self.get_json_body()
        user_logger = UserLogger(self.user_repository)
        try:
            user = user_logger.login_user(body['email'], body['password'])
            auth_info = UserToken.from_user(user)
        except InvalidLoginException:
            return Response.bad_request(message='Invalid email or password')
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred while logging in user')
        return Response.success({'token': auth_info.encode()})

    @route(http_methods.GET, alias='get_data')
    def get_logged_user_data(self) -> Response:
        user_obtainer = UserObtainer(self.user_repository)
        try:
            user = user_obtainer.get_user(self.get_authenticated_user_id())
        except InvalidUserException:
            return Response.bad_request(message='Invalid user')
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred while trying to obtain user data')
        return Response.success(UserSerializer.serialize(user))

    @route(http_methods.GET)
    def generate_device_token(self, device_id: str) -> Response:
        token_generator = DeviceTokenGenerator(self.device_repository)
        try:
            device_token = token_generator.generate(self.get_authenticated_user_id(), device_id)
        except UnregisteredDeviceException:
            return Response.bad_request(message='Invalid device')
        except Exception as e:
            Logger.error(e)
            return Response.server_error('An error has occurred while logging in user')
        return Response.success({'token': device_token.encode()})
