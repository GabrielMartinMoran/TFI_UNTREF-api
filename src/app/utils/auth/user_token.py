from pymodelio import Attribute
from pymodelio.validators import StringValidator

from src.app.utils.auth.token import Token
from src.common import dates
from src.domain.models.user import User


class UserToken(Token):
    _user_email: Attribute[str](validator=StringValidator())

    @property
    def user_email(self) -> str:
        return self._user_email

    @staticmethod
    def from_user(user: User) -> 'UserToken':
        return UserToken(user_email=user.email)

    @classmethod
    def from_encoded(cls, token: str) -> 'UserToken':
        dict_token = cls._decode_string_token(token)
        timestamp = dict_token.get('timestamp')
        return UserToken(
            user_email=dict_token.get('email'),
            timestamp=dates.to_datetime(timestamp) if timestamp is not None else None
        )

    def encode(self) -> str:
        token = {
            'email': self.user_email,
            'timestamp': dates.to_utc_isostring(self.timestamp)
        }
        return self._encode_dict_token(token)

    @classmethod
    def _get_type_prefix(cls) -> str:
        return 'u'
