from src.models.measure import Measure
from src.utils.validators.string_validator import StringValidator
from src.models.base_model import BaseModel
from src.utils.json_utils import get_json_prop


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

    def to_dict(self):
        return {
            'id': self.device_id,
            'name': self.name,
            'bleId': self.ble_id,
            'measures': [measure.to_dict() for measure in self.measures],
            'active': self.active,
            'turnedOn': self.turned_on
        }

    @staticmethod
    def from_dict(json):
        model = Device(
            json.get('name'),
            json.get('bleId', '').lower(),
            device_id=str(get_json_prop(json, 'id', '_id') or ''),
            active=json.get('active', False),
            turned_on=json.get('turnedOn', False),
        )
        model.measures = [Measure.from_dict(x) for x in json.get('measures', [])]
        if 'createdDate' in json:
            model.created_date = get_json_prop(json, 'createdDate')
        return model
