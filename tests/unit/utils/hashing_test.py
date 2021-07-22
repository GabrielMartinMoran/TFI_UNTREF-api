from src.utils.hashing import hash_password


def test_hash_password_returns_sha256_hashed_string_when_password_provided():
    expected = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'
    actual = hash_password('password')
    assert expected == actual


def test_hash_password_returns_none_when_password_is_none():
    actual = hash_password(None)
    assert actual is None
