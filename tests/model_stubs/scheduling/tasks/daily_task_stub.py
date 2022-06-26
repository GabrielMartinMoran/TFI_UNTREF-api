import random
from datetime import datetime
from typing import List

from src.common import dates
from src.common.weekday import Weekday
from src.domain.models.scheduling.tasks.daily_task import DailyTask
from src.domain.models.scheduling.tasks.task_action import TaskAction

_DEFAULT = object()


class DailyTaskStub:

    def __new__(cls, action: TaskAction = _DEFAULT, moment: datetime = _DEFAULT,
                weekdays: List[Weekday] = _DEFAULT) -> DailyTask:
        return DailyTask(
            action=action if action != _DEFAULT else random.choice([x for x in TaskAction]),
            moment=moment if moment != _DEFAULT else dates.now(),
            weekdays=weekdays if weekdays != _DEFAULT else cls._get_weekdays(),

        )

    @classmethod
    def _get_weekdays(cls) -> List[Weekday]:
        weekdays_amount = random.randint(1, len(Weekday))
        weekdays = []
        possible_weekdays = [x for x in Weekday]
        for x in range(weekdays_amount):
            weekday = random.choice(possible_weekdays)
            possible_weekdays.remove(weekday)
            weekdays.append(weekday)
        return weekdays
