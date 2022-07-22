from abc import ABC, abstractmethod
from typing import List

from src.domain.models.scheduling.tasks.task import Task


class DeviceSchedulerRepository(ABC):

    @abstractmethod
    def set_scheduling_tasks(self, device_id: str, tasks: List[Task]) -> None: pass

    @abstractmethod
    def get_scheduling_tasks(self, device_id: str) -> List[Task]: pass
