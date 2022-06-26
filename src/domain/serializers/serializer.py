from abc import abstractmethod
from typing import Any, List


class Serializer:

    @classmethod
    @abstractmethod
    def serialize(cls, model: Any) -> dict: pass

    @classmethod
    def serialize_all(cls, models: List) -> List[dict]:
        return [cls.serialize(model) for model in models]
