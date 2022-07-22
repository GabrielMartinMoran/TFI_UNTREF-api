from src.domain.mappers.mapper import Mapper
from src.domain.models.measure import Measure


class MeasureMapper(Mapper):

    @classmethod
    def map(cls, data: dict) -> Measure:
        return Measure(
            timestamp=data.get('timestamp'),
            voltage=data.get('voltage'),
            current=data.get('current'),
        )
