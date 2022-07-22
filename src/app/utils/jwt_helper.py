import jwt

from src import config


class JWTHelper:

    @staticmethod
    def decode_token(str_token: str) -> dict:
        return jwt.decode(str_token, config.APP_SECRET, algorithms=[config.HASH_ALGORITHM])

    @staticmethod
    def encode_token(token_data: dict) -> str:
        return jwt.encode(token_data, config.APP_SECRET, algorithm=config.HASH_ALGORITHM)
