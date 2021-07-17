from src.utils.text_formatters import *

def test_snake_to_camel_returns_camelcase_version_of_snakecase_input():    
    expected = 'SnakeToCamel'
    actual = snake_to_camel('snake_to_camel')
    assert expected == actual