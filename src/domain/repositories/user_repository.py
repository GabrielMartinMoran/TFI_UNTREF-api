from abc import ABC, abstractmethod

from src.domain.models.user import User


class UserRepository(ABC):

    @abstractmethod
    def exists(self, user_id: str) -> bool: pass

    @abstractmethod
    def get(self, user_id: str) -> User: pass

    @abstractmethod
    def create(self, user: User) -> None: pass
