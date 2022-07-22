from typing import List
from datetime import timedelta

from src import config
from src.domain.exceptions.unregistered_device_exception import UnregisteredDeviceException
from src.domain.models.measure import Measure
from src.domain.repositories.device_repository import DeviceRepository
from src.domain.repositories.measure_repository import MeasureRepository


class DeviceMeasureSummarizer:

    def __init__(self, device_repository: DeviceRepository, measure_repository: MeasureRepository) -> None:
        self._device_repository = device_repository
        self._measure_repository = measure_repository

    def get_summarized_measures(self, device_id: str, user_id: str, time_interval: int) -> List[Measure]:
        if not self._device_repository.exists_for_user(device_id, user_id):
            raise UnregisteredDeviceException()
        measures = self._measure_repository.get_from_last_minutes(device_id, time_interval)
        return self._summarize_measures(measures, time_interval)

    def get_all_devices_summarized_measures(self, user_id: str, time_interval: int) -> List[Measure]:
        measures = self._measure_repository.get_all_for_user_from_last_minutes(user_id, time_interval)
        return self._summarize_measures(measures, time_interval)

    @classmethod
    def _summarize_measures(cls, measures: List[Measure], time_interval: int) -> List[Measure]:
        if not measures:
            return []
        summarization_minutes_interval = float(time_interval) / float(config.MAX_SUMMARIZED_MEASURES_TO_SHOW)
        time_slices = [measures[0].timestamp + timedelta(minutes=summarization_minutes_interval * x) for x in
                       range(config.MAX_SUMMARIZED_MEASURES_TO_SHOW)]
        grouped_measures = []
        # Clone list
        ungrouped_measures = [measure for measure in measures]
        for dt in time_slices:
            filtered_measures = [measure for measure in ungrouped_measures if measure.timestamp <= dt]
            if not filtered_measures:
                continue
            # Update ungrouped
            ungrouped_measures = [measure for measure in ungrouped_measures if measure not in filtered_measures]
            grouped_measures.append(Measure(
                timestamp=dt,
                current=sum([measure.current for measure in filtered_measures]) / len(filtered_measures),
                voltage=sum([measure.voltage for measure in filtered_measures]) / len(filtered_measures)
            ))

        return grouped_measures
