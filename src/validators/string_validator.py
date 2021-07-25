import re
import math
from src.validators.validator import Validator


class StringValidator(Validator):

    def __init__(self, property_name, min_len=0, max_len=math.inf, fixed_len=None, regex=None, **kwargs) -> None:
        super().__init__(property_name, **kwargs)
        self.min_len = min_len
        self.max_len = max_len
        self.fixed_len = fixed_len
        self.regex = regex

    def is_valid(self, model: object) -> bool:
        value = getattr(model, self.property_name)
        if not value and self.nullable:
            return True
        return value is not None and \
               isinstance(value, str) and \
               len(value) >= self.min_len and \
               len(value) <= self.max_len and \
               (not self.fixed_len or len(value) == self.fixed_len) and \
               (not self.regex or re.compile(self.regex).match(value) is not None)
