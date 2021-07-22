import jwt
from src import config
from src.routing.token_parser import TokenParser

token_data = {
    'username': 'test_user'
}


def create_token(token_data: dict):
    return 'Bearer ' + jwt.encode(token_data, config.APP_SECRET, algorithm=config.HASH_ALGORITHM)


class MockedRequest:
    def __init__(self, token) -> None:
        self.headers = {
            TokenParser.AUTH_HEADER: token
        }


def test_init_parses_tokens_when_called():
    parser = TokenParser(MockedRequest(create_token(token_data)))
    assert token_data == parser.token


def test_init_cant_parse_token_if_it_is_not_bearer():
    parser = TokenParser(MockedRequest(jwt.encode(token_data, config.APP_SECRET, algorithm=config.HASH_ALGORITHM)))
    assert parser.token is None


def test_init_cant_parse_token_if_encoded_token_is_not_valid():
    parser = TokenParser(MockedRequest('Bearer invalid_encoded_token'))
    assert parser.token is None


def test_init_cant_parse_token_if_auth_header_not_exists():
    request = MockedRequest(None)
    parser = TokenParser(request)
    assert parser.token is None


def test_init_cant_parse_token_if_auth_header_is_none():
    request = MockedRequest(None)
    parser = TokenParser(request)
    assert parser.token is None


def test_valid_token_returns_true_when_token_is_not_none():
    parser = TokenParser(MockedRequest(create_token(token_data)))
    assert parser.valid_token()


def test_valid_token_returns_false_when_token_is_none():
    parser = TokenParser(MockedRequest('invalid token'))
    assert not parser.valid_token()


def test_get_token_returns_token_attribute_when_called():
    parser = TokenParser(MockedRequest(create_token(token_data)))
    assert token_data == parser.get_token()
