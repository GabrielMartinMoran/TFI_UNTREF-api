from typing import Optional

from src.app.utils.auth.user_token import UserToken
from src.app.utils.http.response import Response

last_response: Optional[Response] = None
token: Optional[UserToken] = None
user_id: Optional[str] = None
