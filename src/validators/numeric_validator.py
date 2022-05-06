import math
from src.validators.validator import Validator


class NumericValidator(Validator):

    def __init__(self, property_name, expected_type, min_value=-math.inf, max_value=math.inf, **kwargs) -> None:
        super().__init__(property_name, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.expected_type = expected_type

    def is_valid(self, model: object) -> bool:
        value = getattr(model, self.property_name)
        if value is None:
            return self.nullable
        return isinstance(value, self.expected_type) and self.min_value <= value <= self.max_value
