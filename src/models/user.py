from src.utils.validators.string_validator import StringValidator
from src.utils import validation_patterns
from src.models.base_model import BaseModel
from src.utils.hashing import hash_password


class User(BaseModel):
    MIN_USER_LENGTH = 3
    MAX_USER_LENGTH = 32

    MODEL_VALIDATORS = [
        StringValidator('username', min_len=MIN_USER_LENGTH, max_len=MAX_USER_LENGTH),
        StringValidator('email', regex=validation_patterns.EMAIL_VALIDATION_PATTERN),
        StringValidator('password', nullable=True, regex=validation_patterns.PASSWORD_VALIDATION_PATTERN),
        StringValidator('hashed_password', message='password is not valid'),
    ]

    def __init__(self, username: str, email: str, user_id: int = None, password: str = None):
        super().__init__()
        self.username = username
        self.email = email.lower() if email else None
        self.user_id = user_id
        self.password = password
        self.avatar = None
        self.hashed_password = None

    def to_dict(self, include_hashed_password=False, creating_user: bool = False) -> dict:
        result = {
            'username': self.username,
            'email': self.email,
            'id': self.user_id,
            'avatar': self.avatar,
            'created_date': self.created_date
        }
        if include_hashed_password:
            result['hashed_password'] = self.hashed_password
        return result

    @staticmethod
    def from_dict(data: dict) -> 'User':
        model = User(
            data.get('username'),
            data.get('email'),
            user_id=data.get('id') or data.get('user_id'),
            password=data.get('password')
        )
        model.avatar = data.get('avatar')
        if 'created_date' in data:
            model.created_date = data.get('created_date')
        if model.password:
            model.hashed_password = hash_password(model.password)
        else:
            model.hashed_password = data.get('hashed_password')
        return model

    def password_matches(self, non_hashed_password) -> bool:
        return self.hashed_password == hash_password(non_hashed_password)
