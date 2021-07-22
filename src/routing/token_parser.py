import jwt
from src import config


class TokenParser:
    TOKEN_TYPE = 'Bearer'
    AUTH_HEADER = 'Authorization'

    def __init__(self, request) -> None:
        self.request = request
        self.token = None
        self.__parse_token()

    def __parse_token(self) -> None:
        try:
            token = self.__get_token_from_header()
            if not token or self.TOKEN_TYPE not in token:
                return
            token = self.__remove_token_type(token)
            data = self.__decode_token(token)
            self.token = data
            return
        except Exception:
            return

    def __get_token_from_header(self) -> str:
        return self.request.headers[self.AUTH_HEADER]

    def __remove_token_type(self, str_token: str) -> str:
        # +1 por el espacio que sigue luego del tipo
        return str_token[len(self.TOKEN_TYPE) + 1:]

    def __decode_token(self, str_token: str) -> str:
        return jwt.decode(str_token, config.APP_SECRET, algorithms=[config.HASH_ALGORITHM])

    def valid_token(self) -> bool:
        return self.token is not None

    def get_token(self) -> dict:
        return self.token
