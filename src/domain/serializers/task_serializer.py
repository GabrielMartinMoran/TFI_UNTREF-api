from typing import List

from src.common import dates
from src.domain.models.scheduling.tasks.daily_task import DailyTask
from src.domain.models.scheduling.tasks.task import Task


class TaskSerializer:

    @staticmethod
    def serialize_task(task: Task) -> dict:
        serialized = {
            'action': task.action.value,
            'moment': dates.to_utc_isostring(task.moment)
        }
        if isinstance(task, DailyTask):
            serialized['weekdays'] = [x.value for x in task.weekdays]
        return serialized

    @staticmethod
    def serialize_tasks(tasks: List[Task]) -> List[dict]:
        return [TaskSerializer.serialize_task(task) for task in tasks]
