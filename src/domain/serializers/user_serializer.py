from src.domain.models.user import User
from src.domain.serializers.serializer import Serializer


class UserSerializer(Serializer):

    @classmethod
    def serialize(cls, model: User) -> dict:
        return {
            'username': model.username,
            'email': model.email
        }
