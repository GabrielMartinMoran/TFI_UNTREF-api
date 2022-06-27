from typing import Union

from dateutil import parser
from datetime import datetime

from pymodelio import Attribute, pymodelio_model
from pymodelio.validators import DatetimeValidator, FloatValidator


@pymodelio_model
class Measure:
    _ROUND_DECIMALS = 2
    _timestamp: Attribute[datetime](validator=DatetimeValidator())
    _voltage: Attribute[float](validator=FloatValidator(min_value=0))
    _current: Attribute[float](validator=FloatValidator(min_value=0))

    def __before_validate__(self) -> None:
        # Cast timestamp to datetime
        if self._timestamp is not None:
            self._timestamp = self._format_timestamp(self._timestamp)
        # Cast voltage to float
        if self._voltage is not None:
            self._voltage = float(self._voltage)
        # Cast current to float
        if self._current is not None:
            self._current = float(self._current)

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
