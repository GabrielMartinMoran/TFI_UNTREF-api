from src.models.measure import Measure
from src.utils.validators.string_validator import StringValidator
from src.models.base_model import BaseModel


class Device(BaseModel):
    MIN_NAME_LENGTH = 1
    MAX_NAME_LENGTH = 32
    BLE_ID_LENGTH = 36

    MODEL_VALIDATORS = [
        StringValidator('name', min_len=MIN_NAME_LENGTH, max_len=MAX_NAME_LENGTH),
        StringValidator('ble_id', fixed_len=BLE_ID_LENGTH)
    ]

    def __init__(self, name: str, ble_id: str, device_id: str = None, active: bool = False, turned_on: bool = False):
        super().__init__()
        self.name = name
        self.ble_id = ble_id
        self.device_id = device_id
        self.active = active
        self.turned_on = turned_on
        self.measures = []

    def to_dict(self) -> dict:
        return {
            'id': self.device_id,
            'name': self.name,
            'ble_id': self.ble_id,
            'measures': [measure.to_dict() for measure in self.measures],
            'active': self.active,
            'turned_on': self.turned_on
        }

    @staticmethod
    def from_dict(data: dict) -> 'Device':
        model = Device(
            data.get('name'),
            data.get('ble_id').lower() if 'ble_id' in data else None,
            device_id=data.get('id'),
            active=data.get('active', False),
            turned_on=data.get('turned_on', False),
        )
        model.measures = [Measure.from_dict(x) for x in data.get('measures', [])]
        if 'created_date' in data:
            model.created_date = data.get('created_date')
        return model
