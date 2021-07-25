import pytest

from src.validators.float_validator import FloatValidator


class ExampleModel:
    prop_to_validate = None


@pytest.fixture
def model():
    return ExampleModel()


def test_is_valid_returns_false_when_property_value_is_not_float(model):
    model.prop_to_validate = 'prop value'
    validator = FloatValidator('prop_to_validate')
    actual = validator.is_valid(model)
    assert not actual


def test_is_valid_returns_true_when_property_value_is_valid(model):
    model.prop_to_validate = 10.0
    validator = FloatValidator('prop_to_validate')
    actual = validator.is_valid(model)
    assert actual
