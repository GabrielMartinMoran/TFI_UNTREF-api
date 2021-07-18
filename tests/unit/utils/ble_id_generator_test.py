from src.utils.ble_id_generator import ble_idGenerator

def test_generate_ble_id_returns_base64_id_splitted_by_hyphens():
    actual = ble_idGenerator.generate_ble_id()
    possible_chars = [str(x) for x in range(10)]
    possible_chars.extend(['a', 'b', 'c', 'd', 'e', 'f'])
    assert len(ble_idGenerator.BLE_ID_PATTERN) == len(actual)
    for i, x in enumerate(ble_idGenerator.BLE_ID_PATTERN):
        if x == '-':
            assert x == actual[i]
        else:
            assert actual[i].lower() in possible_chars