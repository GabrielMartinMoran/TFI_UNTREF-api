from src.domain.services.devices.ble_id_generator import BleIdGenerator


def test_generate_ble_id_returns_base64_id_splitted_by_hyphens():
    actual = BleIdGenerator.generate_ble_id()
    possible_chars = [str(x) for x in range(10)]
    possible_chars.extend(['a', 'b', 'c', 'd', 'e', 'f'])
    assert len(BleIdGenerator.BLE_ID_PATTERN) == len(actual)
    for i, x in enumerate(BleIdGenerator.BLE_ID_PATTERN):
        if x == '-':
            assert x == actual[i]
        else:
            assert actual[i].lower() in possible_chars
