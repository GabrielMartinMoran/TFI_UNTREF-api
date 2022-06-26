from src.domain.mappers.mapper import Mapper
from src.domain.models.user import User


class UserMapper(Mapper):

    @classmethod
    def map(cls, data: dict) -> User:
        model = User(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            hashed_password=data.get('hashed_password'),
            created_date=data.get('created_date')
        )
        model.avatar = data.get('avatar')
        return model
