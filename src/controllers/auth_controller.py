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
    def login(self) -> dict:
        body = self.get_json_body()
        user = self.user_repository.get_by_email(body['email'])
        if user is None or not user.password_matches(body['password']):
            return self.error('Invalid email or password')
        """
        if not user.verified:
            response = jsonify({'message': 'Account is not verified', 'code' : config.ErrorCodes.ACCOUNT_NOT_VERIFIED})
            response.status_code = 403
            return response
        """
        return self.ok_success({'token': self.generate_jwt(user)})

    def generate_jwt(self, user: User) -> str:
        token_data = {
            'id': user.user_id,
            'email': user.email,
            'timestamp': datetime.datetime.utcnow().timestamp()
        }
        return jwt.encode(token_data, config.APP_SECRET, algorithm=config.HASH_ALGORITHM)

    @http_method(http_methods.POST)
    def verify_account(self, user_id: str) -> dict:
        if not user_id:
            return self.validation_error('No userId provided')
        body = self.get_json_body()
        if not 'verificationToken' in body:
            return self.validation_error('No verificationToken provided')
        verified = False
        try:
            verified = self.user_repository.verify_user(user_id, body['verificationToken'])
        except Exception as ex:
            return self.error(F'An error has occured while trying to verify user with id {user_id}')
        if not verified:
            return self.validation_error(F'Invalid userId or verificationToken')
        return self.ok_success()

    @http_method(http_methods.GET, auth_required=True)
    def get_renewed_token(self) -> dict:
        user = User()
        user.email = self.token['email']
        user.user_id = self.get_authenticated_user_id()
        return self.ok_success({'token': self.generate_jwt(user)})
