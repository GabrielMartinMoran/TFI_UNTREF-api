from src.utils.validators.numeric_validator import NumericValidator


class FloatValidator(NumericValidator):

    def __init__(self, property_name, **kwargs) -> None:
        super().__init__(property_name, float, **kwargs)