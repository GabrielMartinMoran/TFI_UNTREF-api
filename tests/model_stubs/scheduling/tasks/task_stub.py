import random
from datetime import datetime

from src.common import dates
from src.domain.models.scheduling.tasks.task import Task
from src.domain.models.scheduling.tasks.task_action import TaskAction

_DEFAULT = object()


class TaskStub:

    def __new__(cls, action: TaskAction = _DEFAULT, moment: datetime = _DEFAULT) -> Task:
        return Task(
            action=action if action != _DEFAULT else random.choice([x for x in TaskAction]),
            moment=moment if moment != _DEFAULT else dates.now()
        )
