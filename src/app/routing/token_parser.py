from src.app.utils.auth_info import AuthInfo


class TokenParser:
    TOKEN_TYPE = 'Bearer'
    AUTH_HEADER = 'Authorization'

    def __init__(self, request) -> None:
        self._request = request
        self._auth_info = None
        self.__parse_token()

    @property
    def auth_info(self) -> AuthInfo:
        return self._auth_info

    def __parse_token(self) -> None:
        try:
            token = self.__get_token_from_header()
            if not token or self.TOKEN_TYPE not in token:
                return
            token = self.__remove_token_type(token)
            self._auth_info = AuthInfo.from_token(token)
        except Exception:
            pass

    def __get_token_from_header(self) -> str:
        return self._request.headers[self.AUTH_HEADER]

    def __remove_token_type(self, str_token: str) -> str:
        # +1 por el espacio que sigue luego del tipo
        return str_token[len(self.TOKEN_TYPE) + 1:]

    def valid_token(self) -> bool:
        return self.auth_info is not None
