import datetime
import jwt
from src.controllers.base_controller import BaseController
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.utils.http import http_methods
from src.utils.http.response import Response
from src.utils.http.route import route
from src import config


class AuthController(BaseController):

    def __init__(self) -> None:
        super().__init__()
        self.user_repository = UserRepository()

    @route(http_methods.POST)
    def register(self) -> Response:
        user = User.from_dict(self.get_json_body())
        if not user.is_valid():
            return self.validation_error(user.validation_errors)
        if self.user_repository.email_exists(user.email):
            return self.error('User with same email already exists')
        try:
            self.user_repository.insert(user)
        except Exception as ex:
            return self.error('An error has ocurred while creating user')
        return self.created_ok()

    @route(http_methods.POST)
    def login(self) -> Response:
        body = self.get_json_body()
        user = self.user_repository.get_by_email(body['email'])
        if user is None or not user.password_matches(body['password']):
            return self.error('Invalid email or password')
        return self.ok({'token': self.generate_jwt(user)})

    # TODO: Mover de aqui
    def generate_jwt(self, user: User) -> str:
        token_data = {
            'id': user.user_id,
            'email': user.email,
            'timestamp': datetime.datetime.utcnow().timestamp()
        }
        return jwt.encode(token_data, config.APP_SECRET, algorithm=config.HASH_ALGORITHM)

    @route(http_methods.GET, auth_required=True)
    def get_renewed_token(self) -> Response:
        user = User()
        user.email = self.token['email']
        user.user_id = self.get_authenticated_user_id()
        return self.ok({'token': self.generate_jwt(user)})

    @route(http_methods.GET, auth_required=True)
    def get_logged_user_data(self) -> Response:
        user_id = self.get_authenticated_user_id()
        user = self.user_repository.get_by_id(user_id, get_avatar=True)
        if not user:
            return self.error('Invalid user')
        return self.ok(user.to_dict())