from src.models.measure import Measure
from .base_repository import BaseRepository


class MeasureRepository(BaseRepository):

    def insert(self, measure: Measure, ble_id: str, user_id: int) -> None:
        # TODO: Cambiar el tipo de dato del timestamp a datetime
        self._execute_query(f"INSERT INTO Measures (device_id, voltage, current, timestamp) VALUES ("
                            f"(SELECT device_id FROM Devices WHERE user_id = {user_id} AND ble_id = '{ble_id}'), "
                            f"{measure.voltage}, {measure.current}, to_timestamp({measure.timestamp}))")

    def get_last_measures(self, ble_id: str, user_id: str, time_interval: int):
        res = self._execute_query(f"SELECT * FROM Measures WHERE device_id = "
                                  f"(SELECT device_id FROM Devices WHERE ble_id = '{ble_id}' "
                                  f"AND user_id = '{user_id}')"
                                  f"AND timestamp::TIMESTAMP >= "
                                  f"(now()::TIMESTAMP - INTERVAL '{time_interval} min')")
        measures = res.to_model_list(Measure(0, 0, 0))
        # Convert timestamps to int
        for measure in measures:
            measure.timestamp = int(measure.timestamp.timestamp())
        return measures
