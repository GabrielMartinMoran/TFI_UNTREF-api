import pytest
from src.utils.validators.numeric_validator import NumericValidator


class ExampleModel:
    prop_to_validate = None


@pytest.fixture
def model():
    return ExampleModel()


def test_is_valid_returns_true_when_property_value_is_none_and_property_is_nullable(model):
    validator = NumericValidator('prop_to_validate', int, nullable=True)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_false_when_property_value_is_none_and_property_is_not_nullable(model):
    validator = NumericValidator('prop_to_validate', int)
    actual = validator.is_valid(model)
    assert not actual


def test_is_valid_returns_false_when_property_value_is_not_provided_type(model):
    model.prop_to_validate = 10
    validator = NumericValidator('prop_to_validate', float)
    actual = validator.is_valid(model)
    assert not actual


def test_is_valid_returns_false_when_property_value_is_lower_than_min(model):
    model.prop_to_validate = 10
    validator = NumericValidator('prop_to_validate', int, min=11)
    actual = validator.is_valid(model)
    assert not actual


def test_is_valid_returns_true_when_property_value_is_valid_and_value_is_greater_than_min(model):
    model.prop_to_validate = 10
    validator = NumericValidator('prop_to_validate', int, min=9)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_true_when_property_value_is_valid_and_value_is_equal_to_min(model):
    model.prop_to_validate = 10
    validator = NumericValidator('prop_to_validate', int, min=10)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_false_when_property_value_is_greater_than_max(model):
    model.prop_to_validate = 10
    validator = NumericValidator('prop_to_validate', int, max=9)
    actual = validator.is_valid(model)
    assert not actual


def test_is_valid_returns_true_when_property_value_is_valid_and_value_is_lower_than_max(model):
    model.prop_to_validate = 10
    validator = NumericValidator('prop_to_validate', int, max=11)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_true_when_property_value_is_valid_and_value_is_equal_to_max(model):
    model.prop_to_validate = 10
    validator = NumericValidator('prop_to_validate', int, max=10)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_true_when_property_value_is_valid(model):
    model.prop_to_validate = 10
    validator = NumericValidator('prop_to_validate', int)
    actual = validator.is_valid(model)
    assert actual
