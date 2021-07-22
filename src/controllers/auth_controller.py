from src.controllers.base_controller import BaseController
from src.exceptions.email_already_registered_exception import EmailAlreadyRegisteredException
from src.exceptions.invalid_login_exception import InvalidLoginException
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.services.auth.user_logger import UserLogger
from src.services.auth.user_registerer import UserRegisterer
from src.utils.http import http_methods
from src.utils.http.response import Response
from src.utils.http.route import route


class AuthController(BaseController):

    def __init__(self) -> None:
        super().__init__()
        self.user_repository = UserRepository()

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
        except Exception:
            return self.error('An error has occurred while creating user')
        return self.created_ok()

    @route(http_methods.POST)
    def login(self) -> Response:
        body = self.get_json_body()
        user_logger = UserLogger(self.user_repository)
        try:
            jwt_token = user_logger.login_user(body['email'], body['password'])
        except InvalidLoginException:
            return self.error('Invalid email or password')
        except Exception:
            return self.error('An error has occurred while logging in user')
        return self.ok({'token': jwt_token})

    @route(http_methods.GET, auth_required=True)
    def get_logged_user_data(self) -> Response:
        user_id = self.get_authenticated_user_id()
        user = self.user_repository.get_by_id(user_id, get_avatar=True)
        if not user:
            return self.error('Invalid user')
        return self.ok(user.to_dict())
