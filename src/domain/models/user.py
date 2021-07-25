from src.common.id_generator import IdGenerator
from src.validators import validation_patterns
from src.domain.models.base_model import BaseModel
from src.common.hashing import hash_password
from src.validators.string_validator import StringValidator


class User(BaseModel):
    MIN_USER_LENGTH = 3
    MAX_USER_LENGTH = 32

    MODEL_VALIDATORS = [
        StringValidator('username', min_len=MIN_USER_LENGTH, max_len=MAX_USER_LENGTH),
        StringValidator('email', regex=validation_patterns.EMAIL_VALIDATION_PATTERN),
        StringValidator('_password', nullable=True, regex=validation_patterns.PASSWORD_VALIDATION_PATTERN,
                        message='password is not valid'),
        StringValidator('hashed_password', message='password is not valid'),
    ]

    def __init__(self, username: str, email: str, password: str = None, hashed_password: str = None):
        super().__init__()
        self._username = username
        self._email = email.lower() if email else None
        self._password = password
        self._hashed_password = hash_password(password) if password else hashed_password

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def id(self) -> str:
        return User.email_to_id(self.email)

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    def to_dict(self, include_hashed_password=False, creating_user: bool = False) -> dict:
        result = {
            'username': self.username,
            'email': self.email
        }
        if include_hashed_password:
            result['hashed_password'] = self.hashed_password
        return result

    @staticmethod
    def from_dict(data: dict) -> 'User':
        model = User(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            hashed_password=data.get('hashed_password')
        )
        model.avatar = data.get('avatar')
        if 'created_date' in data:
            model._created_date = data.get('created_date')
        return model

    @staticmethod
    def email_to_id(email: str) -> str:
        return IdGenerator.generate_id(email)

    def password_matches(self, non_hashed_password) -> bool:
        return self.hashed_password == hash_password(non_hashed_password)
