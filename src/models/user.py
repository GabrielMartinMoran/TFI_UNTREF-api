from src.utils.validators.string_validator import StringValidator
from src.utils import validation_patterns
from src.models.base_model import BaseModel
from src.utils.json_utils import get_json_prop
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

    def to_dict(self, include_hashed_password=False, creating_user: bool = False):
        result = {
            'username': self.username,
            'email': self.email,
            'id': self.user_id,
            'avatar': self.avatar,
            'createdDate': self.created_date
        }
        if include_hashed_password:
            result['hashedPassword'] = self.hashed_password
        return result

    @staticmethod
    def from_dict(json) -> 'User':
        model = User(
            json.get('username'),
            json.get('email'),
            user_id=str(get_json_prop(json, 'id', '_id')),
            password=json.get('password')
        )
        model.avatar = get_json_prop(json, 'avatar')
        if 'createdDate' in json:
            model.created_date = json.get('createdDate')
        if model.password:
            model.hashed_password = hash_password(model.password)
        else:
            model.hashed_password = json.get('hashedPassword')
        return model

    def password_matches(self, non_hashed_password) -> bool:
        return self.hashed_password == hash_password(non_hashed_password)
