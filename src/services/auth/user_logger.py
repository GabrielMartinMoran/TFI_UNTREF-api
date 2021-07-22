from datetime import datetime

import jwt

from src import config
from src.exceptions.invalid_login_exception import InvalidLoginException
from src.models.user import User
from src.repositories.user_repository import UserRepository


class UserLogger:

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def login_user(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)
        if user is None or not user.password_matches(password):
            raise InvalidLoginException()
        return self._generate_jwt(user)

    def _generate_jwt(self, user: User) -> str:
        token_data = {
            'id': user.user_id,
            'email': user.email,
            'timestamp': datetime.utcnow().timestamp()
        }
        return jwt.encode(token_data, config.APP_SECRET, algorithm=config.HASH_ALGORITHM)
