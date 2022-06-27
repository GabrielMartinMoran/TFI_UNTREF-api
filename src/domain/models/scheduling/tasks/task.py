from datetime import datetime

from pymodelio import Attribute, pymodelio_model
from pymodelio.validators import Validator, DatetimeValidator

from src.common import dates
from src.domain.models.scheduling.scheduler_action import SchedulerAction
from src.domain.models.scheduling.tasks.task_action import TaskAction


@pymodelio_model
class Task:
    """
    A task that is executed just one time
    """
    _action: Attribute[TaskAction](validator=Validator(expected_type=TaskAction))
    _moment: Attribute[datetime](validator=DatetimeValidator())

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
