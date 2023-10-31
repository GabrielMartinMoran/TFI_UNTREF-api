from datetime import datetime
from typing import Optional

from src.common import dates
from src.domain.models.scheduling.tasks.task_action import TaskAction
from src.domain.repositories.instant_action_repository import InstantActionRepository
from src.infrastructure.repositories.postgres_repository import PostgresRepository


class InstantActionPGRepository(PostgresRepository, InstantActionRepository):
    def clean_for(self, device_id: str) -> None:
        self._execute_query(f"DELETE FROM InstantActions WHERE device_id='{device_id}'")

    def push(self, device_id: str, action: TaskAction) -> None:
        self._execute_query(f"INSERT INTO InstantActions (device_id, action, timestamp) VALUES "
                            f"('{device_id}', '{action.value}', CURRENT_TIMESTAMP)")

    def pull(self, device_id: str, pull_until: datetime) -> Optional[TaskAction]:
        result = self._execute_query(f"SELECT * FROM InstantActions WHERE device_id = '{device_id}'"
                                     f"AND timestamp::TIMESTAMP >= '{dates.to_utc_isostring(pull_until)}'::TIMESTAMP")
        if len(result.rows) == 0:
            return None
        action = result.first()['action']
        return TaskAction(action)
