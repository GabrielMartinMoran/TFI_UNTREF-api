from .postgres_repository import PostgresRepository
from ...domain.mappers.user_mapper import UserMapper
from ...domain.models.user import User
from ...domain.repositories.user_repository import UserRepository


class UserPGRepository(PostgresRepository, UserRepository):

    def exists(self, user_id: str) -> bool:
        result = self._execute_query(f"SELECT COUNT(user_id) AS count FROM Users WHERE user_id = '{user_id}'")
        return result.first()['count'] > 0

    def get(self, user_id: str) -> User:
        result = self._execute_query(f"SELECT * FROM Users WHERE user_id = '{user_id}'")
        return result.map_first(UserMapper)

    def create(self, user: User) -> None:
        self._execute_query(f"INSERT INTO Users (user_id, username, email, hashed_password) VALUES "
                            f"('{user.user_id}', '{user.username}', '{user.email}', '{user.hashed_password}')")
