from datetime import timezone
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
        last_status_update = data.get('last_status_update')
        if last_status_update is not None:
            last_status_update = last_status_update.replace(tzinfo=timezone.utc)
        return Device(
            name=data.get('name'),
            device_id=device_id,
            turned_on=data.get('turned_on', False),
            measures=MeasureMapper.map_all(data.get('measures', [])),
            last_status_update=last_status_update
        )

    @classmethod
    def map_all(cls, data: List[dict], set_id: bool = False) -> List[Device]:
        return [cls.map(element, set_id) for element in data]
