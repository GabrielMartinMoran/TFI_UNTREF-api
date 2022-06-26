from datetime import datetime

from src.common import dates
from src.domain.models import BaseModel
from src.domain.models.scheduling.scheduler_action import SchedulerAction
from src.domain.models.scheduling.tasks.task_action import TaskAction
from src.validators.datetime_validator import DatetimeValidator
from src.validators.validator import Validator


class Task(BaseModel):
    """
    A task that is executed just one time
    """

    MODEL_VALIDATORS = [
        Validator('action'),
        DatetimeValidator('moment')
    ]

    def __init__(self, action: TaskAction, moment: datetime) -> None:
        self._action = action
        self._moment = moment
        super().__init__()

    @property
    def action(self) -> TaskAction:
        return self._action

    @property
    def moment(self) -> datetime:
        return self._moment

    def get_next_scheduler_action(self) -> SchedulerAction:
        return SchedulerAction(
            action=self.action,
            moment=self.moment
        )

    @property
    def has_passed(self) -> bool:
        """
        Returns true if the task moment already passed
        """
        return dates.now() > self.moment

    def to_dict(self) -> dict:
        pass
