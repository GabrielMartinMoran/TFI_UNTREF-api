from src.common import dates
from src.domain.models.scheduling.scheduler_action import SchedulerAction
from src.domain.serializers.serializer import Serializer


class SchedulerActionSerializer(Serializer):

    @classmethod
    def serialize(cls, model: SchedulerAction, use_epochs: bool = False) -> dict:
        return {
            'action': model.action.value,
            'moment': dates.to_utc_isostring(model.moment) if not use_epochs else dates.to_timestamp(model.moment)
        }
