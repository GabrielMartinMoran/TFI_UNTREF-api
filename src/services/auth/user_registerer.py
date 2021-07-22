from src.exceptions.email_already_registered_exception import EmailAlreadyRegisteredException
from src.models.user import User
from src.repositories.user_repository import UserRepository


class UserRegisterer:

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def register_user(self, user: User) -> None:
        if self._user_repository.email_exists(user.email):
            raise EmailAlreadyRegisteredException()
        self._user_repository.insert(user)
