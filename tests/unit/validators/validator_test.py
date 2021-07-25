import pytest

from src.validators.validator import Validator


class ExampleModel:
    prop_to_validate = None


@pytest.fixture
def model():
    return ExampleModel()


def test_is_valid_returns_true_when_property_value_is_not_none(model):
    model.prop_to_validate = 'Not None'
    validator = Validator('prop_to_validate')
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_true_when_property_value_is_none_and_property_is_nullable(model):
    validator = Validator('prop_to_validate', nullable=True)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_false_when_property_value_is_none_and_property_is_not_nullable(model):
    validator = Validator('prop_to_validate')
    actual = validator.is_valid(model)
    assert not actual


def test_get_failed_message_returns_default_message_when_message_was_not_specified(model):
    expected = 'prop_to_validate is not valid'
    validator = Validator('prop_to_validate')
    actual = validator.get_failed_message()
    assert actual == expected


def test_get_failed_message_returns_custom_message_when_message_was_specified(model):
    expected = 'provided property is not valid'
    validator = Validator('prop_to_validate', message=expected)
    actual = validator.get_failed_message()
    assert actual == expected
