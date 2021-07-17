from src.models.measure import Measure
from .base_repository import BaseRepository


class MeasureRepository(BaseRepository):

    def insert(self, measure: Measure, ble_id: str, user_id: int) -> None:
        # TODO: Cambiar el tipo de dato del timestamp a datetime
        self._execute_query(f"INSERT INTO Measures (device_id, voltage, current, timestamp) VALUES ("
                            f"(SELECT device_id FROM Devices WHERE user_id = {user_id} AND ble_id = '{ble_id}'), "
                            f"{measure.voltage}, {measure.current}, to_timestamp({measure.timestamp}))"
        )
