from typing import List

from src.common import dates
from src.common.weekday import Weekday
from src.domain.models.scheduling.tasks.daily_task import DailyTask
from src.domain.models.scheduling.tasks.task import Task
from src.domain.models.scheduling.tasks.task_action import TaskAction


class TaskMapper:

    @staticmethod
    def map_tasks(tasks: List[dict]) -> List[Task]:
        mapped_tasks = []
        for task in tasks:
            action = TaskAction(task.get('action'))
            moment = dates.to_datetime(task.get('moment')) if 'moment' in task else None
            if 'weekdays' in task:
                mapped_tasks.append(DailyTask(
                    action=action,
                    moment=moment,
                    weekdays=[Weekday(x) for x in task.get('weekdays', [])]
                ))
            else:
                mapped_tasks.append(Task(
                    action=action,
                    moment=moment
                ))
        return mapped_tasks
