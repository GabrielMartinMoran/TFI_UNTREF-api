from src.utils.validators.numeric_validator import NumericValidator


class IntValidator(NumericValidator):

    def __init__(self, property_name, **kwargs) -> None:
        super().__init__(property_name, int, **kwargs)
