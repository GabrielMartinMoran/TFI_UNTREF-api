from datetime import datetime
from typing import List, Optional

from pymodelio import Attr, PymodelioModel
from pymodelio.validators import StringValidator

from src.common import dates
from src.common.id_generator import IdGenerator
from src.domain.models.measure import Measure


class Device(PymodelioModel):
    MIN_NAME_LENGTH = 1
    MAX_NAME_LENGTH = 50
    BLE_ID_LENGTH = 36

    IS_ACTIVE_SECONDS_DELTA = 20

    _name: Attr(str, init_alias='name', validator=StringValidator(min_len=MIN_NAME_LENGTH, max_len=MAX_NAME_LENGTH))
    _device_id: Attr(str, init_alias='device_id', validator=StringValidator(fixed_len=BLE_ID_LENGTH),
                     default_factory=IdGenerator.generate_unique_id)
    _turned_on: Attr(bool, init_alias='turned_on', default_factory=lambda: False)
    _measures: Attr(List[Measure], init_alias='measures', default_factory=list)
    _last_status_update: Attr(Optional[datetime], init_alias='last_status_update')  # noqa: F821

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
        if self._last_status_update is None:
            return False
        return abs((self._last_status_update - dates.now()).total_seconds()) <= self.IS_ACTIVE_SECONDS_DELTA

    @property
    def turned_on(self) -> bool:
        return self._turned_on

    @property
    def measures(self) -> List[Measure]:
        return self._measures
