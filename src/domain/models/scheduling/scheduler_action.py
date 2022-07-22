from datetime import datetime

from src.domain.models.scheduling.tasks.task_action import TaskAction


class SchedulerAction:

    def __init__(self, action: TaskAction, moment: datetime) -> None:
        self._action = action
        self._moment = moment

    @property
    def action(self) -> TaskAction:
        return self._action

    @property
    def moment(self) -> datetime:
        return self._moment
