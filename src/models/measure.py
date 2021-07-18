from src.utils.validators.int_validator import IntValidator
from src.utils.validators.float_validator import FloatValidator
from src.models.base_model import BaseModel


class Measure(BaseModel):
    MODEL_VALIDATORS = [
        IntValidator('timestamp', min=0),
        FloatValidator('voltage', min=0),
        FloatValidator('current', min=0),
    ]

    def __init__(self, timestamp: int, voltage: float, current: float):
        super().__init__()
        self.timestamp = timestamp
        self.voltage = voltage
        self.current = current

    def to_dict(self) -> dict:
        return {
            'timestamp': self.timestamp,
            'voltage': self.voltage,
            'current': self.current
        }

    @staticmethod
    def from_dict(data: dict) -> 'Measure':
        model = Measure(
            data.get('timestamp'),
            data.get('voltage'),
            data.get('current'),
        )
        if isinstance(model.voltage, int):
            model.voltage = float(model.voltage)
        if isinstance(model.current, int):
            model.current = float(model.current)
        return model
