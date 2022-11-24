from pymodelio import Attribute, pymodelio_model
from pymodelio.validators import StringValidator

from src.app.utils.auth.permission_level import PermissionLevel
from src.app.utils.auth.token import Token
from src.common import dates


@pymodelio_model
class DeviceToken(Token):
    _device_id: Attribute[str](validator=StringValidator())
    _user_id: Attribute[str](validator=StringValidator())

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @classmethod
    def from_encoded(cls, token: str) -> 'DeviceToken':
        dict_token = cls._decode_string_token(token)
        timestamp = dict_token.get('timestamp')
        return DeviceToken(
            device_id=dict_token.get('device_id'),
            user_id=dict_token.get('user_id'),
            timestamp=dates.to_datetime(timestamp) if timestamp is not None else None
        )

    def encode(self) -> str:
        token = {
            'device_id': self.device_id,
            'user_id': self.user_id,
            'timestamp': dates.to_utc_isostring(self.timestamp)
        }
        return self._encode_dict_token(token)

    @classmethod
    def _get_type_prefix(cls) -> str:
        return 'd'

    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.DEVICE
