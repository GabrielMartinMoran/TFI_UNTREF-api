from typing import Union

from dateutil import parser
from datetime import datetime

from src.validators.datetime_validator import DatetimeValidator
from src.validators.float_validator import FloatValidator
from src.domain.models.base_model import BaseModel


class Measure(BaseModel):
    MODEL_VALIDATORS = [
        DatetimeValidator('timestamp'),
        FloatValidator('voltage', min=0),
        FloatValidator('current', min=0),
    ]

    def __init__(self, timestamp: Union[datetime, int, str], voltage: Union[int, float],
                 current: Union[int, float]):
        super().__init__()
        self._timestamp = self._format_timestamp(timestamp) if timestamp else None
        self._voltage = float(voltage) if voltage else None
        self._current = float(current) if current else None

    def _format_timestamp(self, timestamp: Union[datetime, int, str]) -> datetime:
        if isinstance(timestamp, datetime):
            return timestamp
        if isinstance(timestamp, str):
            return parser.parse(timestamp)
        if isinstance(timestamp, int):
            return datetime.fromtimestamp(timestamp)
        raise ValueError('invalid timestamp')

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def voltage(self):
        return self._voltage

    @property
    def current(self):
        return self._current

    @property
    def power(self):
        return self.voltage * self.current

    def to_dict(self) -> dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'voltage': self.voltage,
            'current': self.current,
            'power': self.power
        }

    @staticmethod
    def from_dict(data: dict) -> 'Measure':
        return Measure(
            timestamp=data.get('timestamp'),
            voltage=data.get('voltage'),
            current=data.get('current'),
        )
