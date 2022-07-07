from typing import List

from pymodelio import UNDEFINED

from src.domain.mappers.mapper import Mapper
from src.domain.mappers.measure_mapper import MeasureMapper
from src.domain.models.device import Device


class DeviceMapper(Mapper):

    @classmethod
    def map(cls, data: dict, set_id: bool = False) -> Device:
        device_id = data.get('device_id', data.get('id'))
        if not set_id or device_id is None:
            device_id = UNDEFINED
        return Device(
            name=data.get('name'),
            device_id=device_id,
            active=data.get('active', False),
            turned_on=data.get('turned_on', False),
            measures=MeasureMapper.map_all(data.get('measures', [])),
            created_date=data.get('created_date')
        )

    @classmethod
    def map_all(cls, data: List[dict], set_id: bool = False) -> List[Device]:
        return [cls.map(element, set_id) for element in data]
