from src.app.routing.token_parser import TokenParser
from src.app.utils.auth.user_token import UserToken


def create_token(user_email: dict):
    return 'Bearer ' + UserToken(user_email=user_email).encode()


class MockedRequest:
    def __init__(self, token) -> None:
        self.headers = {
            TokenParser.AUTH_HEADER: token
        }


def test_init_parses_tokens_when_called():
    parser = TokenParser(MockedRequest(create_token('test@test.com')))
    assert parser.token.user_email == 'test@test.com'


def test_init_cant_parse_token_if_it_is_not_bearer():
    parser = TokenParser(MockedRequest(UserToken(user_email='test@test.com').encode()))
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


def test_valid_token_returns_true_when_token_is_valid():
    parser = TokenParser(MockedRequest(create_token('test@test.com')))
    assert parser.valid_token()


def test_valid_token_returns_false_when_token_is_not_valid():
    parser = TokenParser(MockedRequest('invalid auth_info'))
    assert not parser.valid_token()
