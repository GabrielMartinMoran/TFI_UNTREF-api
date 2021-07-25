import math
from src.validators.validator import Validator


class NumericValidator(Validator):

    def __init__(self, property_name, expected_type, min=-math.inf, max=math.inf, **kwargs) -> None:
        super().__init__(property_name, **kwargs)
        self.min = min
        self.max = max
        self.expected_type = expected_type

    def is_valid(self, model: object) -> bool:
        value = getattr(model, self.property_name)
        if value is None and self.nullable:
            return True
        return value is not None and \
               isinstance(value, self.expected_type) and \
               value >= self.min and \
               value <= self.max
