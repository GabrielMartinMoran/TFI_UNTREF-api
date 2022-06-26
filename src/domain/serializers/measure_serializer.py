from src.common import dates
from src.domain.models.measure import Measure
from src.domain.serializers.serializer import Serializer


class MeasureSerializer(Serializer):

    @classmethod
    def serialize(cls, model: Measure) -> dict:
        return {
            'timestamp': dates.to_utc_isostring(model.timestamp),
            'voltage': model.voltage,
            'current': model.current,
            'power': model.power
        }
