import random
from typing import List

from src.common.id_generator import IdGenerator
from src.domain.models.device import Device
from src.domain.models.measure import Measure

_DEFAULT = object()


def _generate_device_name():
    return random.choice(['Heladera', 'lampara', 'Microondas', 'Dispenser de agua'])


class DeviceStub:

    def __new__(cls, name: str = _DEFAULT, device_id: str = _DEFAULT, active: bool = _DEFAULT,
                turned_on: bool = _DEFAULT, measures: List[Measure] = []) -> Device:
        return Device(
            name if name != _DEFAULT else _generate_device_name(),
            device_id if device_id != _DEFAULT else IdGenerator.generate_unique_id(),
            active if active != _DEFAULT else random.choice([True, False]),
            turned_on if turned_on != _DEFAULT else random.choice([True, False]),
            measures
        )
