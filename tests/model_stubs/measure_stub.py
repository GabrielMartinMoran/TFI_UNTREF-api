import random
from datetime import datetime

from src.common import dates
from src.domain.models.measure import Measure

_DEFAULT = object()


class MeasureStub:
    def __new__(cls, timestamp: datetime = _DEFAULT, voltage: float = _DEFAULT, current: bool = _DEFAULT) -> Measure:
        return Measure(
            timestamp if timestamp != _DEFAULT else dates.now(),
            voltage if voltage != _DEFAULT else random.uniform(0.0, 230.0),
            current if current != _DEFAULT else random.uniform(0.0, 20.0)
        )
