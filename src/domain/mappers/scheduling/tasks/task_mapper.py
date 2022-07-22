from src.common import dates
from src.common.weekday import Weekday
from src.domain.mappers.mapper import Mapper
from src.domain.models.scheduling.tasks.daily_task import DailyTask
from src.domain.models.scheduling.tasks.task import Task
from src.domain.models.scheduling.tasks.task_action import TaskAction


class TaskMapper(Mapper):

    @classmethod
    def map(cls, data: dict) -> Task:
        action = TaskAction(data.get('action'))
        moment = dates.to_datetime(data.get('moment')) if 'moment' in data else None
        if 'weekdays' in data:
            return DailyTask(
                action=action,
                moment=moment,
                weekdays=[Weekday(x) for x in data.get('weekdays', [])]
            )
        return Task(
            action=action,
            moment=moment
        )
