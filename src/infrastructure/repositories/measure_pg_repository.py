from typing import List

from .postgres_repository import PostgresRepository
from ...domain.models.measure import Measure
from ...domain.repositories.measure_repository import MeasureRepository


class MeasurePGRepository(PostgresRepository, MeasureRepository):

    def create(self, measure: Measure, device_id: str) -> None:
        self._execute_query(f"INSERT INTO Measures (device_id, voltage, current, timestamp) VALUES ("
                            f"'{device_id}', {measure.voltage}, {measure.current}, '{measure.timestamp}')")

    def get_from_last_minutes(self, device_id: str, time_interval: int) -> List[Measure]:
        result = self._execute_query(f"SELECT * FROM Measures WHERE device_id = '{device_id}'"
                                     f"AND timestamp::TIMESTAMP >= (now()::TIMESTAMP - INTERVAL '{time_interval} min')")
        return result.map_all(Measure)
