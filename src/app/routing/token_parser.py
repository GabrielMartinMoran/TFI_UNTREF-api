from src.app.utils.auth.device_token import DeviceToken
from src.app.utils.auth.token import Token
from src.app.utils.auth.user_token import UserToken


class TokenParser:
    TOKEN_TYPE = 'Bearer'
    AUTH_HEADER = 'Authorization'

    def __init__(self, request) -> None:
        self._request = request
        self._token = None
        self.__parse_token()

    @property
    def token(self) -> Token:
        return self._token

    def __parse_token(self) -> None:
        try:
            token = self.__get_token_from_header()
            if not token or self.TOKEN_TYPE not in token:
                return
            token = self.__remove_token_type(token)
            for token_type in {UserToken, DeviceToken}:
                if token_type.is_encoded_form(token):
                    self._token = token_type.from_encoded(token)
        except Exception:
            pass

    def __get_token_from_header(self) -> str:
        return self._request.headers[self.AUTH_HEADER]

    def __remove_token_type(self, str_token: str) -> str:
        # +1 por el espacio que sigue luego del tipo
        return str_token[len(self.TOKEN_TYPE) + 1:]

    def valid_token(self) -> bool:
        return self.token is not None
