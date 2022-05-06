from typing import List
import datetime

from src.common import dates
from src.domain.exceptions.model_validation_exception import ModelValidationException
from src.validators.validator import Validator


class BaseModel:
    MODEL_VALIDATORS: List[Validator] = []

    def __init__(self, created_date: datetime.datetime = None) -> None:
        """
        The call to this method by a child class should be done at the end of the child constructor because the
        validator is called automatically.
        """
        self._created_date = dates.now() if created_date is None else created_date
        self.validate()

    @property
    def created_date(self) -> datetime.datetime:
        return self._created_date

    def to_dict(self) -> dict:
        raise NotImplementedError()

    def validate(self) -> None:
        validation_errors = []
        for validator in self.MODEL_VALIDATORS:
            if not validator.is_valid(self):
                validation_errors.append(validator.get_failed_message())
        if validation_errors:
            raise ModelValidationException(validation_errors)

    @staticmethod
    def from_dict(data: dict) -> 'BaseModel':
        return BaseModel(created_date=data.get('created_date'))
