from typing import List, Optional

from src.domain.models.scheduling.scheduler_action import SchedulerAction
from src.domain.models.scheduling.tasks.task import Task


class SchedulingStack:

    def __init__(self, tasks: List[Task] = None) -> None:
        self._tasks = tasks or []

    @property
    def tasks(self) -> List[Task]:
        return self._tasks

    def get_next_action(self) -> Optional[SchedulerAction]:
        actions = [x.get_next_scheduler_action() for x in self.tasks if not x.has_passed]
        if not actions:
            return None
        actions = sorted(actions, key=lambda x: x.moment)
        return actions[0]
