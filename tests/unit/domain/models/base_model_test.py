import pytest
from src.domain.models import BaseModel


@pytest.fixture
def base_model():
    return BaseModel()


"""
def test_to_json_raise_exception_when_not_implemented(base_model):
    with pytest.raises(NotImplementedError):
        base_model.to_dict()
"""

"""
def test_is_valid_does_not_raise_error_when_the_model_is_valid(base_model):
    base_model.to_dict = lambda x: {}
    base_model.validate()
"""

"""
def test_from_json_returns_base_model_instance_when_json_provided():
    json = {'created_date': 1000}
    actual = BaseModel.from_dict(json)
    assert actual.created_date == json['created_date']
"""
