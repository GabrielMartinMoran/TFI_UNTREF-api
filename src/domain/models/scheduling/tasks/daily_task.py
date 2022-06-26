from datetime import datetime, timedelta
from typing import List

from src.common import dates
from src.domain.exceptions.model_validation_exception import ModelValidationException
from src.domain.models.scheduling.scheduler_action import SchedulerAction
from src.common.weekday import Weekday
from src.domain.models.scheduling.tasks.task import Task
from src.domain.models.scheduling.tasks.task_action import TaskAction


class DailyTask(Task):
    """
    A task that is executed in specific days
    On daily tasks, moment is used as time, not datetime
    """

    def __init__(self, action: TaskAction, moment: datetime, weekdays: List[Weekday]) -> None:
        if len(weekdays) == 0:
            raise ModelValidationException('weekdays attribute can not be empty')
        self._weekdays = weekdays
        super().__init__(action, moment)

    @property
    def weekdays(self) -> List[Weekday]:
        return self._weekdays

    def get_next_scheduler_action(self) -> SchedulerAction:
        now = dates.now()
        current_weekday = Weekday(dates.now().weekday())
        task_weekday = Weekday.next_after(current_weekday) if now.time() > self.moment.time() else current_weekday
        task_moment = now + timedelta(days=Weekday.days_between(current_weekday, task_weekday))
        return SchedulerAction(
            action=self.action,
            moment=task_moment
        )

    @property
    def has_passed(self) -> bool:
        """
        Daily tasks never pass because the next valid day is returned
        """
        return False
