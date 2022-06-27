from pymodelio import UNDEFINED

from src.domain.mappers.mapper import Mapper
from src.domain.mappers.measure_mapper import MeasureMapper
from src.domain.models.device import Device


class DeviceMapper(Mapper):

    @classmethod
    def map(cls, data: dict, set_id: bool = False) -> Device:
        return Device(
            name=data.get('name'),
            device_id=data.get('device_id', data.get('id')) if data.get('device_id',
                                                                        data.get('id')) and set_id else UNDEFINED,
            active=data.get('active', False),
            turned_on=data.get('turned_on', False),
            measures=MeasureMapper.map_all(data.get('measures', [])),
            created_date=data.get('created_date')
        )
