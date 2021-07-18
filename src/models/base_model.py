from typing import List

from src.utils.json_utils import get_json_prop
import datetime

from src.utils.validators.validator import Validator


class BaseModel:
    MODEL_VALIDATORS: List[Validator] = []

    def __init__(self) -> None:
        self.validation_errors = []
        self.created_date = datetime.datetime.now()

    def is_valid(self) -> bool:
        self.validate()
        return len(self.validation_errors) == 0

    def to_dict(self) -> dict:
        raise NotImplementedError()

    def validate(self) -> None:
        self.validation_errors = []
        for validator in self.MODEL_VALIDATORS:
            if not validator.is_valid(self):
                self.validation_errors.append(validator.get_failed_message())

    @staticmethod
    def from_dict(data: dict) -> 'BaseModel':
        model = BaseModel()
        if 'created_date' in data:
            model.created_date = get_json_prop(data, 'created_date')
        return model
