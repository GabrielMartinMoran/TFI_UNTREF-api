from src.utils.image_encoder import ImageEncoder


def test_to_base_64_str_returns_base64_string_when_image_provided():
    actual = ImageEncoder.to_base_64_str(b'000')
    assert ImageEncoder.BASE_64_ENCODING_PREFIX in actual


def test_to_base_64_str_returns_none_when_image_is_none():
    actual = ImageEncoder.to_base_64_str(None)
    assert actual is None
