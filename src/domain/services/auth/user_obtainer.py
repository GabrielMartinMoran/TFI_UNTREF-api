from src.domain.exceptions.invalid_user_exception import InvalidUserException
from src.domain.models.user import User
from src.domain.repositories.user_repository import UserRepository


class UserObtainer:

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def get_user(self, user_id: str) -> User:
        user = self._user_repository.get(user_id)
        if not user:
            raise InvalidUserException()
        return user
