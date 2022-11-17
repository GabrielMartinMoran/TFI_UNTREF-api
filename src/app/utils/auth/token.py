from abc import abstractmethod
from datetime import datetime

from pymodelio import Attribute, pymodelio_model
from pymodelio.validators import DatetimeValidator

from src.app.utils.jwt_helper import JWTHelper
from src.common import dates


@pymodelio_model
class Token:
    _timestamp: Attribute[datetime](validator=DatetimeValidator(), default_factory=dates.now)

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @staticmethod
    @abstractmethod
    def from_encoded(token: str) -> 'Token':
        pass

    @abstractmethod
    def encode(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def _get_type_prefix(cls) -> str:
        pass

    def _encode_dict_token(self, data: dict) -> str:
        return f'{self._get_type_prefix()}{JWTHelper.encode_token(data)}'

    @classmethod
    def _decode_string_token(cls, token: str) -> dict:
        normalized_token = cls._clean_type_prefix(token)
        return JWTHelper.decode_token(normalized_token)

    @classmethod
    def _clean_type_prefix(cls, token: str) -> str:
        if not cls.is_encoded_form(token):
            raise AssertionError('Token does not have the required prefix')
        return token[len(cls._get_type_prefix()):]

    @classmethod
    def is_encoded_form(cls, token: str) -> bool:
        return token.startswith(cls._get_type_prefix())
