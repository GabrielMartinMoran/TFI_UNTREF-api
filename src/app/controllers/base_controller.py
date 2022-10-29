from typing import Optional

from src.app.utils.auth_info import AuthInfo
from src.app.utils.http.request import Request
from src.domain.models.user import User


class BaseController:

    def __init__(self, request: Request, auth_info: AuthInfo = None) -> None:
        self._request = request
        self._auth_info = auth_info

    def get_json_body(self):
        return self._request.body

    def get_authenticated_user_id(self) -> Optional[str]:
        if not self._auth_info:
            return None
        return User.email_to_id(self._auth_info.user_email)

    def get_query_param(self, name: str, default: Optional[str] = None) -> str:
        return self._request.query_params.get(name, default)
