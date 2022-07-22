from datetime import datetime
from dateutil import parser

from src.domain.models.user import User
from src.app.utils.jwt_helper import JWTHelper


class AuthInfo:

    def __init__(self, user_email: str, timestamp: datetime = None) -> None:
        self._user_email = user_email
        self._timestamp = timestamp if timestamp else datetime.utcnow()

    @property
    def user_email(self) -> str:
        return self._user_email

    @staticmethod
    def from_token(token: str) -> 'AuthInfo':
        decoded_token = JWTHelper.decode_token(token)
        return AuthInfo(
            user_email=decoded_token['email'],
            timestamp=parser.parse(decoded_token['timestamp'])
        )

    @staticmethod
    def from_user(user: User) -> 'AuthInfo':
        return AuthInfo(user.email)

    def to_token(self) -> str:
        token_data = {
            'email': self.user_email,
            'timestamp': self._timestamp.isoformat()
        }
        return JWTHelper.encode_token(token_data)
