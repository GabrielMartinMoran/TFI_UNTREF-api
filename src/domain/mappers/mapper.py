from abc import abstractmethod
from typing import Any, List


class Mapper:

    @classmethod
    @abstractmethod
    def map(cls, data: dict) -> Any: pass

    @classmethod
    def map_all(cls, data: List[dict]) -> List:
        return [cls.map(element) for element in data]
