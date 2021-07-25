"""
from src.common.id_generator import generate_unique_id, ID_LENGTH


def test_generate_unique_id_returns_24_length_string():
    actual = generate_unique_id()
    assert len(actual) == ID_LENGTH


def test_generate_unique_id_returns_hexadecimal_string():
    actual = generate_unique_id()
    possible_chars = [str(x) for x in range(10)]
    possible_chars.extend(['a', 'b', 'c', 'd', 'e', 'f'])
    for x in actual:
        assert str(x).lower() in possible_chars
"""
