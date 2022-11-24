from typing import Optional

from src.app.utils.auth.device_token import DeviceToken
from src.app.utils.auth.token import Token
from src.app.utils.auth.user_token import UserToken
from src.app.utils.http.request import Request
from src.domain.models.user import User


class BaseController:

    def __init__(self, request: Request, token: Optional[Token] = None) -> None:
        self._request = request
        self._token = token

    def get_json_body(self):
        return self._request.body

    def get_authenticated_user_id(self) -> Optional[str]:
        if not self._token:
            return None
        if isinstance(self._token, UserToken):
            return User.email_to_id(self._token.user_email)
        if isinstance(self._token, DeviceToken):
            return self._token.user_id
        return None

    def _validate_device_permission(self, device_id: str) -> str:
        if not isinstance(self._token, DeviceToken):
            # If the token is not a device one, this method doesn't matter
            return
        if device_id != self._token.device_id:
            raise PermissionError()

    def get_query_param(self, name: str, default: Optional[str] = None) -> str:
        return self._request.query_params.get(name, default)
