from decimal import Decimal
from typing import Union

from dateutil import parser
from datetime import datetime

from src.common import dates
from src.domain.exceptions.model_validation_exception import ModelValidationException
from src.validators.datetime_validator import DatetimeValidator
from src.validators.float_validator import FloatValidator
from src.domain.models.base_model import BaseModel


class Measure(BaseModel):
    _ROUND_DECIMALS = 2

    MODEL_VALIDATORS = [
        DatetimeValidator('timestamp'),
        FloatValidator('voltage', min_value=0),
        FloatValidator('current', min_value=0),
    ]

    def __init__(self, timestamp: Union[datetime, int, str], voltage: Union[int, float],
                 current: Union[int, float, Decimal], *args, **kwargs):
        self._timestamp = self._format_timestamp(timestamp) if timestamp else None
        if not isinstance(voltage, (float, int, Decimal)):
            raise ModelValidationException('voltage must be a valid float or int')
        self._voltage = float(voltage)
        if not isinstance(current, (float, int, Decimal)):
            raise ModelValidationException('current must be a valid float or int')
        self._current = float(current)
        super().__init__(*args, **kwargs)

    @classmethod
    def _format_timestamp(cls, timestamp: Union[datetime, int, str]) -> datetime:
        if isinstance(timestamp, datetime):
            return timestamp
        if isinstance(timestamp, str):
            return parser.parse(timestamp)
        if isinstance(timestamp, int):
            return datetime.utcfromtimestamp(timestamp)
        raise ValueError('invalid timestamp')

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def voltage(self) -> float:
        return round(self._voltage, self._ROUND_DECIMALS)

    @property
    def current(self) -> float:
        return round(self._current, self._ROUND_DECIMALS)

    @property
    def power(self) -> float:
        return round(self.voltage * self.current, self._ROUND_DECIMALS)

    def to_dict(self) -> dict:
        return {
            'timestamp': dates.to_utc_isostring(self.timestamp),
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
