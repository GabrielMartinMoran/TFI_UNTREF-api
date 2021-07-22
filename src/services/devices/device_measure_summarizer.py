from typing import List
from datetime import timedelta

from src.exceptions.unregistered_device_exception import UnregisteredDeviceException
from src.models.measure import Measure
from src.repositories.device_repository import DeviceRepository
from src.repositories.measure_repository import MeasureRepository


class DeviceMeasureSummarizer:
    MAX_MEASURES_TO_RETURN = 50

    def __init__(self, device_repository: DeviceRepository, measure_repository: MeasureRepository) -> None:
        self._device_repository = device_repository
        self._measure_repository = measure_repository

    def get_summarized_measures(self, ble_id: str, user_id: str, time_interval: int) -> List[Measure]:
        if not self._device_repository.ble_id_exists_for_user(ble_id, user_id):
            raise UnregisteredDeviceException()
        measures = self._measure_repository.get_last_measures(ble_id, user_id, time_interval)
        return self._summarize_measures(measures, time_interval)

    def _summarize_measures(self, measures: List[Measure], time_interval: int):
        if not measures:
            return []
        summarization_minutes_interval = float(time_interval) / float(self.MAX_MEASURES_TO_RETURN)
        time_slices = [measures[0].time + timedelta(minutes=summarization_minutes_interval * x) for x in
                       range(self.MAX_MEASURES_TO_RETURN)]
        grouped_measures = []
        # Clone list
        ungrouped_measures = [measure for measure in measures]
        for dt in time_slices:
            filtered_measures = [measure for measure in ungrouped_measures if measure.time <= dt]
            if not filtered_measures:
                continue
            # Update ungrouped
            ungrouped_measures = [measure for measure in ungrouped_measures if measure not in filtered_measures]
            grouped_measures.append(Measure(
                timestamp=int(dt.timestamp()),
                current=float(sum([measure.current for measure in filtered_measures]) / len(filtered_measures)),
                voltage=float(sum([measure.voltage for measure in filtered_measures]) / len(filtered_measures))
            ))

        return grouped_measures
