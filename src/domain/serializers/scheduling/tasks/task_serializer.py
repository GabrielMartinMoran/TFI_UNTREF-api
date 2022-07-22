from src.common import dates
from src.domain.models.scheduling.tasks.daily_task import DailyTask
from src.domain.models.scheduling.tasks.task import Task
from src.domain.serializers.serializer import Serializer


class TaskSerializer(Serializer):

    @classmethod
    def serialize(cls, model: Task) -> dict:
        serialized = {
            'action': model.action.value,
            'moment': dates.to_utc_isostring(model.moment)
        }
        if isinstance(model, DailyTask):
            serialized['weekdays'] = [x.value for x in model.weekdays]
        return serialized
