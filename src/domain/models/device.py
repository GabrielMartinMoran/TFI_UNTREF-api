from typing import List

from src.common.id_generator import IdGenerator
from src.domain.models.measure import Measure
from src.validators.string_validator import StringValidator
from src.domain.models.base_model import BaseModel


class Device(BaseModel):
    MIN_NAME_LENGTH = 1
    MAX_NAME_LENGTH = 32
    BLE_ID_LENGTH = 36

    MODEL_VALIDATORS = [
        StringValidator('name', min_len=MIN_NAME_LENGTH, max_len=MAX_NAME_LENGTH),
        StringValidator('_id', fixed_len=BLE_ID_LENGTH, message='device id is not valid')
    ]

    def __init__(self, name: str, device_id: str = None, active: bool = False, turned_on: bool = False,
                 measures: List[Measure] = []):
        super().__init__()
        self._name = name
        self._id = device_id.lower() if device_id else IdGenerator.generate_unique_id()
        self._active = active
        self._turned_on = turned_on
        self._measures = measures

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._id

    @property
    def active(self) -> bool:
        return self._active

    @property
    def turned_on(self) -> bool:
        return self._turned_on

    @property
    def measures(self) -> List[Measure]:
        return self._measures

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'measures': [measure.to_dict() for measure in self.measures],
            'active': self.active,
            'turned_on': self.turned_on
        }

    @staticmethod
    def from_dict(data: dict, set_id=True) -> 'Device':
        model = Device(
            name=data.get('name'),
            device_id=data.get('id') if data.get('id') and set_id else None,
            active=data.get('active', False),
            turned_on=data.get('turned_on', False),
            measures=[Measure.from_dict(x) for x in data.get('measures', [])]
        )
        if 'created_date' in data:
            model.created_date = data.get('created_date')
        return model
