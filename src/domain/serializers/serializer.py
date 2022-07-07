from abc import abstractmethod
from typing import Any, List


class Serializer:

    @classmethod
    @abstractmethod
    def serialize(cls, model: Any, **kwargs) -> dict: pass

    @classmethod
    def serialize_all(cls, models: List, **kwargs) -> List[dict]:
        return [cls.serialize(model, **kwargs) for model in models]
