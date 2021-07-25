from src.app.controllers.base_controller import BaseController
from src.app.utils.jwt_helper import JWTHelper
from src.domain.exceptions.email_already_registered_exception import EmailAlreadyRegisteredException
from src.domain.exceptions.invalid_login_exception import InvalidLoginException
from src.domain.services.auth.user_logger import UserLogger
from src.domain.services.auth.user_registerer import UserRegisterer
from src.app.utils.http import http_methods
from src.app.utils.http.response import Response
from src.app.utils.http.route import route
from src.infrastructure.repositories.user_pg_repository import UserPGRepository
from src.domain.models.user import User


class AuthController(BaseController):

    def __init__(self) -> None:
        super().__init__()
        self.user_repository = UserPGRepository()

    @route(http_methods.POST)
    def register(self) -> Response:
        user = User.from_dict(self.get_json_body())
        if not user.is_valid():
            return self.validation_error(user.validation_errors)
        user_registerer = UserRegisterer(self.user_repository)
        try:
            user_registerer.register_user(user)
        except EmailAlreadyRegisteredException:
            return self.error('User with same email already exists')
        except Exception as e:
            print(e)
            return self.error('An error has occurred while creating user')
        return self.created_ok()

    @route(http_methods.POST)
    def login(self) -> Response:
        body = self.get_json_body()
        user_logger = UserLogger(self.user_repository)
        try:
            token_data = user_logger.login_user(body['email'], body['password'])
            jwt_token = JWTHelper.encode_token(token_data)
        except InvalidLoginException:
            return self.error('Invalid email or password')
        except Exception as e:
            print(e)
            return self.error('An error has occurred while logging in user')
        return self.ok({'token': jwt_token})

    """
    @route(http_methods.GET, auth_required=True)
    def get_logged_user_data(self) -> Response:
        user_id = self.get_authenticated_user_id()
        user = self.user_repository.get_by_id(user_id, get_avatar=True)
        if not user:
            return self.error('Invalid user')
        return self.ok(user.to_dict())
    """
