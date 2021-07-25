from datetime import datetime

from src.validators.validator import Validator


class DatetimeValidator(Validator):

    def is_valid(self, model: object) -> bool:
        value = getattr(model, self.property_name)
        return (value and isinstance(value, datetime)) or super().is_valid(model)
