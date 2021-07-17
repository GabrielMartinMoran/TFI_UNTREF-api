from src.utils.json_utils import get_json_prop
import datetime


class BaseModel:
    MODEL_VALIDATORS = []

    def __init__(self):
        self.validation_errors = []
        self.created_date = datetime.datetime.now()

    def is_valid(self) -> bool:
        self.validate()
        return len(self.validation_errors) == 0

    def to_dict(self) -> dict:
        raise NotImplementedError()

    def validate(self):
        self.validation_errors = []
        for validator in self.MODEL_VALIDATORS:
            if not validator.is_valid(self):
                self.validation_errors.append(validator.get_failed_message())

    @staticmethod
    def from_dict(json):
        model = BaseModel()
        if 'createdDate' in json:
            model.created_date = get_json_prop(json, 'createdDate')
        return model
