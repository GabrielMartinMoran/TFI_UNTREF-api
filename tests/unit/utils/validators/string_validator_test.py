import pytest
from src.utils.validators.string_validator import StringValidator
from src.utils import validation_patterns


class ExampleModel:
    prop_to_validate = None


@pytest.fixture
def model():
    return ExampleModel()


def test_is_valid_returns_true_when_property_value_is_none_and_property_is_nullable(model):
    validator = StringValidator('prop_to_validate', nullable=True)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_false_when_property_value_is_none_and_property_is_not_nullable(model):
    validator = StringValidator('prop_to_validate')
    actual = validator.is_valid(model)
    assert not actual


def test_is_valid_returns_false_when_property_value_is_not_string(model):
    model.prop_to_validate = 123
    validator = StringValidator('prop_to_validate')
    actual = validator.is_valid(model)
    assert not actual


def test_is_valid_returns_false_when_property_value_length_is_lower_than_min_len(model):
    model.prop_to_validate = 'test text'
    validator = StringValidator('prop_to_validate', min_len=10)
    actual = validator.is_valid(model)
    assert not actual


def test_is_valid_returns_true_when_property_value_is_valid_and_length_is_greater_than_min_len(model):
    model.prop_to_validate = 'test text'
    validator = StringValidator('prop_to_validate', min_len=8)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_true_when_property_value_is_valid_and_length_is_equal_to_min_len(model):
    model.prop_to_validate = 'test text'
    validator = StringValidator('prop_to_validate', min_len=9)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_false_when_property_value_length_is_greater_than_max_len(model):
    model.prop_to_validate = 'test text'
    validator = StringValidator('prop_to_validate', max_len=8)
    actual = validator.is_valid(model)
    assert not actual


def test_is_valid_returns_true_when_property_value_is_valid_and_length_is_lower_than_max_len(model):
    model.prop_to_validate = 'test text'
    validator = StringValidator('prop_to_validate', max_len=10)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_true_when_property_value_is_valid_and_length_is_equal_to_max_len(model):
    model.prop_to_validate = 'test text'
    validator = StringValidator('prop_to_validate', max_len=9)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_false_when_property_value_length_is_different_than_fixed_len(model):
    model.prop_to_validate = 'test text'
    validator = StringValidator('prop_to_validate', fixed_len=10)
    actual = validator.is_valid(model)
    assert not actual


def test_is_valid_returns_true_when_property_value_is_valid_and_length_is_equal_to_fixed_len(model):
    model.prop_to_validate = 'test text'
    validator = StringValidator('prop_to_validate', fixed_len=9)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_false_when_property_value_does_not_match_regex(model):
    model.prop_to_validate = 'test text'
    validator = StringValidator('prop_to_validate', regex=validation_patterns.EMAIL_VALIDATION_PATTERN)
    actual = validator.is_valid(model)
    assert not actual


def test_is_valid_returns_true_when_property_is_valid_and_value_matches_regex(model):
    model.prop_to_validate = 'test@test.com'
    validator = StringValidator('prop_to_validate', regex=validation_patterns.EMAIL_VALIDATION_PATTERN)
    actual = validator.is_valid(model)
    assert actual


def test_is_valid_returns_true_when_property_value_is_valid(model):
    model.prop_to_validate = 'Not None'
    validator = StringValidator('prop_to_validate')
    actual = validator.is_valid(model)
    assert actual
