import json
from typing import List

from src.domain.mappers.device_mapper import DeviceMapper
from src.domain.mappers.scheduling.tasks.task_mapper import TaskMapper
from src.domain.models.device import Device
from src.domain.models.scheduling.tasks.task import Task
from src.domain.repositories.device_repository import DeviceRepository
from src.domain.serializers.scheduling.tasks.task_serializer import TaskSerializer
from src.infrastructure.repositories.postgres_repository import PostgresRepository


class DevicePGRepository(PostgresRepository, DeviceRepository):

    def create(self, device: Device, user_id: int) -> None:
        self._execute_query(f"INSERT INTO Devices (device_id, user_id, name, active, turned_on) VALUES "
                            f"('{device.id}', '{user_id}', '{device.name}', {device.active}, {device.turned_on})")

    def exists_for_user(self, device_id: str, user_id: int) -> bool:
        res = self._execute_query(f"SELECT COUNT(device_id) FROM Devices WHERE device_id = '{device_id}' AND "
                                  f"user_id = '{user_id}'")
        return res.first()['count'] > 0

    def get_user_devices(self, user_id: str) -> List[Device]:
        res = self._execute_query(f"SELECT * FROM Devices WHERE user_id = '{user_id}'")
        return res.map_all(DeviceMapper)

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
