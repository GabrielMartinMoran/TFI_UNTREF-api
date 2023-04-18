from typing import List

from pymodelio import Attr, PymodelioModel
from pymodelio.validators import StringValidator

from src.common.id_generator import IdGenerator
from src.domain.models.measure import Measure


class Device(PymodelioModel):
    MIN_NAME_LENGTH = 1
    MAX_NAME_LENGTH = 50
    BLE_ID_LENGTH = 36
    _name: Attr(str, validator=StringValidator(min_len=MIN_NAME_LENGTH, max_len=MAX_NAME_LENGTH))
    _device_id: Attr(str, validator=StringValidator(fixed_len=BLE_ID_LENGTH),
                     default_factory=IdGenerator.generate_unique_id)
    _active: Attr(bool, default_factory=lambda: False)
    _turned_on: Attr(bool, default_factory=lambda: False)
    _measures: Attr(List[Measure], default_factory=list)

    def __before_validate__(self) -> None:
        # Force the device_id to be lowercase
        self._device_id = self._device_id.lower()

    @property
    def name(self) -> str:
        return self._name

    @property
    def device_id(self) -> str:
        return self._device_id

    @property
    def active(self) -> bool:
        return self._active

    @property
    def turned_on(self) -> bool:
        return self._turned_on

    @property
    def measures(self) -> List[Measure]:
        return self._measures
