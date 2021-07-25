from src.domain.exceptions.email_already_registered_exception import EmailAlreadyRegisteredException
from src.domain.models.user import User
from src.domain.repositories.user_repository import UserRepository


class UserRegisterer:

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def register_user(self, user: User) -> None:
        if self._user_repository.exists(user.id):
            raise EmailAlreadyRegisteredException()
        self._user_repository.create(user)
