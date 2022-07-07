from src.domain.models.device import Device
from src.domain.serializers.measure_serializer import MeasureSerializer
from src.domain.serializers.serializer import Serializer


class DeviceSerializer(Serializer):

    @classmethod
    def serialize(cls, model: Device) -> dict:
        return {
            'device_id': model.device_id,
            'name': model.name,
            'measures': MeasureSerializer.serialize_all(model.measures),
            'active': model.active,
            'turned_on': model.turned_on
        }
