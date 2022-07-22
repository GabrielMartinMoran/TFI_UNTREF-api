from abc import ABC, abstractmethod
from typing import List

from src.domain.models.measure import Measure


class MeasureRepository(ABC):

    @abstractmethod
    def create(self, measure: Measure, device_id: str) -> None: pass

    @abstractmethod
    def get_from_last_minutes(self, device_id: str, time_interval: int) -> List[Measure]: pass

    @abstractmethod
    def get_all_for_user_from_last_minutes(self, user_id: str, time_interval: int) -> List[Measure]: pass
