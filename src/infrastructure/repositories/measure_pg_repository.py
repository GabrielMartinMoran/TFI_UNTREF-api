from typing import List

from src.domain.mappers.measure_mapper import MeasureMapper
from src.domain.models.measure import Measure
from src.domain.repositories.measure_repository import MeasureRepository
from src.infrastructure.repositories.postgres_repository import PostgresRepository


class MeasurePGRepository(PostgresRepository, MeasureRepository):

    def create(self, measure: Measure, device_id: str) -> None:
        self._execute_query(f"INSERT INTO Measures (device_id, voltage, current, timestamp) VALUES ("
                            f"'{device_id}', {measure.voltage}, {measure.current}, '{measure.timestamp}')")

    def create_multiple(self, measures: List[Measure], device_id: str) -> None:
        if not measures:
            return
        values = ', '.join([
            f"('{device_id}', {measure.voltage}, {measure.current}, '{measure.timestamp}')" for measure in measures
        ])
        self._execute_query(f"INSERT INTO Measures (device_id, voltage, current, timestamp) VALUES {values}")

    def get_from_last_minutes(self, device_id: str, time_interval: int) -> List[Measure]:
        result = self._execute_query(f"SELECT * FROM Measures WHERE device_id = '{device_id}'"
                                     f"AND timestamp::TIMESTAMP >= (now()::TIMESTAMP - INTERVAL '{time_interval} min')")
        return result.map_all(MeasureMapper)

    def get_all_for_user_from_last_minutes(self, user_id: str, time_interval: int) -> List[Measure]:
        result = self._execute_query("SELECT M.* FROM Measures M, Devices D WHERE M.device_id = D.device_id AND "
                                     f"D.user_id = '{user_id}' AND "
                                     f"M.timestamp::TIMESTAMP >= (now()::TIMESTAMP - INTERVAL '{time_interval} min')")
        return result.map_all(MeasureMapper)
