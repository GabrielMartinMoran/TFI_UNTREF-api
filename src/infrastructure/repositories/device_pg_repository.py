from typing import List

from .postgres_repository import PostgresRepository
from ...domain.models.device import Device
from ...domain.repositories.device_repository import DeviceRepository


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
        return res.map_all(Device)
