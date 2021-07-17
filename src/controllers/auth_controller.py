import datetime
import jwt
from flask import jsonify
from src.controllers.base_controller import BaseController, http_method
from src.repositories.user_repository import UserRepository
from src.models.user import User
import src.config as config
from src.utils import http_methods
from src import config


class AuthController(BaseController):

    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()

    @http_method(http_methods.POST)
    def register(self) -> dict:
        user = User.from_dict(self.get_json_body())
        if not user.is_valid():
            return self.validation_error(user.validation_errors)
        if self.user_repository.email_exists(user.email):
            return self.error('User with same email already exists')
        try:
            self.user_repository.insert(user)
        except Exception as ex:
            return self.error('An error has ocurred while creating user')
        return self.ok_success()

    @http_method(http_methods.POST)
    def login(self) -> dict:
        body = self.get_json_body()
        user = self.user_repository.get_by_email(body['email'])
        if user is None or not user.password_matches(body['password']):
            return self.error('Invalid email or password')
        return self.ok_success({'token': self.generate_jwt(user)})

    def generate_jwt(self, user: User) -> str:
        token_data = {
            'id': user.user_id,
            'email': user.email,
            'timestamp': datetime.datetime.utcnow().timestamp()
        }
        return jwt.encode(token_data, config.APP_SECRET, algorithm=config.HASH_ALGORITHM)

    @http_method(http_methods.GET, auth_required=True)
    def get_renewed_token(self) -> dict:
        user = User()
        user.email = self.token['email']
        user.user_id = self.get_authenticated_user_id()
        return self.ok_success({'token': self.generate_jwt(user)})

    @http_method(http_methods.GET, auth_required=True)
    def get_logged_user_data(self) -> dict:
        user_id = self.get_authenticated_user_id()
        user = self.user_repository.get_by_id(user_id, get_avatar=True)
        if not user:
            return self.error('Invalid user')
        return self.ok_success(user.to_dict())