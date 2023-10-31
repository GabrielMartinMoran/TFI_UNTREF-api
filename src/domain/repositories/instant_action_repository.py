from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from src.domain.models.scheduling.tasks.task_action import TaskAction


class InstantActionRepository(ABC):

    @abstractmethod
    def push(self, device_id: str, action: TaskAction) -> None: pass

    @abstractmethod
    def pull(self, device_id: str, pull_until: datetime) -> Optional[TaskAction]: pass

    @abstractmethod
    def clean_for(self, device_id: str) -> None: pass
