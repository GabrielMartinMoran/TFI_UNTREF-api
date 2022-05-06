class Validator:

    def __init__(self, property_name, nullable=False, message=None) -> None:
        self.property_name = property_name
        self.nullable = nullable
        self.message = message or f'{property_name} is not valid'

    def is_valid(self, model: object) -> bool:
        return getattr(model, self.property_name) is not None or self.nullable

    def get_failed_message(self) -> str:
        return self.message
