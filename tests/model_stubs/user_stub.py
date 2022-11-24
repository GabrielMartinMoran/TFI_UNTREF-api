import random
import string

from src.domain.models.user import User

_EMAIL_DOMAINS = ['gmail.com', 'hotmail.co.uk', 'yandex.ru']
_LOWERCASE_LETTERS = list(string.ascii_lowercase)
_UPPERCASE_LETTERS = list(string.ascii_uppercase)
_DIGITS = list(string.digits)
_EMAIL_CHARACTERS = _DIGITS + _LOWERCASE_LETTERS + _UPPERCASE_LETTERS + list('._')
_MAX_EMAIL_HEAD_SIZE = 64
_VALID_USERNAME_CHARACTERS = [x for x in list(string.printable) if x not in ['\t', '\n', '\r', '\x0b', '\x0c']]


def _generate_random_email() -> str:
    email_head = ''
    for x in range(random.randint(1, _MAX_EMAIL_HEAD_SIZE)):
        email_head += random.choice(_EMAIL_CHARACTERS)
    # Email can not start with '.'
    while email_head.startswith('.') or email_head.startswith('_'):
        email_head = random.choice(_EMAIL_CHARACTERS) + email_head[1:]
    return f'{email_head}@{random.choice(_EMAIL_DOMAINS)}'


def _generate_random_username() -> str:
    username = ''
    for x in range(random.randint(User.MIN_USERNAME_LENGTH, User.MAX_USERNAME_LENGTH)):
        username += random.choice(_VALID_USERNAME_CHARACTERS)
    return username


def _generate_random_password() -> str:
    password = ''
    lists_to_choice_chars = [_LOWERCASE_LETTERS, _UPPERCASE_LETTERS, _DIGITS]
    i = random.randint(0, 2)
    for x in range(random.randint(8, 32)):
        password += random.choice(lists_to_choice_chars[i])
        i += 1
        if i == 3:
            i = 0
    return password


_DEFAULT = object()


class UserStub:

    def __new__(cls, username: str = _DEFAULT, email: str = _DEFAULT, password: str = _DEFAULT,
                hashed_password: str = _DEFAULT) -> User:
        return User(
            username=username if username != _DEFAULT else _generate_random_username(),
            email=email if email != _DEFAULT else _generate_random_email(),
            password=password if password != _DEFAULT else _generate_random_password(),
            hashed_password=hashed_password if hashed_password != _DEFAULT else None
        )
