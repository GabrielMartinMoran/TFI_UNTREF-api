from typing import Union, List


class ModelValidationException(Exception):

    def __init__(self, validation_errors: Union[str, List[str]]) -> None:
        if isinstance(validation_errors, str):
            self.validation_errors = [validation_errors]
        else:
            self.validation_errors = validation_errors
