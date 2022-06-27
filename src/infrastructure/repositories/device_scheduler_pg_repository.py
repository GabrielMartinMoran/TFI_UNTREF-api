import json
from typing import List

from src.domain.mappers.scheduling.tasks.task_mapper import TaskMapper
from src.domain.models.scheduling.tasks.task import Task
from src.domain.repositories.device_scheduler_repository import DeviceSchedulerRepository
from src.domain.serializers.scheduling.tasks.task_serializer import TaskSerializer
from src.infrastructure.repositories.postgres_repository import PostgresRepository


class DeviceSchedulerPGRepository(PostgresRepository, DeviceSchedulerRepository):

    def _has_scheduling_tasks(self, device_id: str) -> bool:
        res = self._execute_query(f"SELECT COUNT(device_id) FROM DeviceTasks WHERE device_id = '{device_id}'")
        return res.first()['count'] > 0

    def _create_scheduling_tasks(self, device_id: str, tasks: List[Task]) -> bool:
        serialized_tasks = json.dumps(TaskSerializer.serialize_all(tasks))
        self._execute_query(f"INSERT INTO DeviceTasks (device_id, tasks) VALUES ('{device_id}', '{serialized_tasks}')")

    def _update_scheduling_tasks(self, device_id: str, tasks: List[Task]) -> bool:
        serialized_tasks = json.dumps(TaskSerializer.serialize_all(tasks))
        self._execute_query(f"UPDATE DeviceTasks SET tasks='{serialized_tasks}' WHERE device_id='{device_id}'")

    def set_scheduling_tasks(self, device_id: str, tasks: List[Task]) -> None:
        if not self._has_scheduling_tasks(device_id):
            self._create_scheduling_tasks(device_id, tasks)
        else:
            self._update_scheduling_tasks(device_id, tasks)

    def get_scheduling_tasks(self, device_id: str) -> List[Task]:
        res = self._execute_query(f"SELECT tasks FROM DeviceTasks WHERE device_id = '{device_id}'")
        if not res.records:
            return []
        return TaskMapper.map_all(res.first()['tasks'])
