import datetime
import random

class BLEIdGenerator:

    BLE_ID_PATTERN = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    TIMESTAMP_MULTIPLIER = 1000000

    @staticmethod
    def generate_ble_id():
        chars_lenght = len(BLEIdGenerator.BLE_ID_PATTERN.replace('-', ''))
        unique = BLEIdGenerator.__generate_unique_id(chars_lenght)
        ble_id = ''
        for char in BLEIdGenerator.BLE_ID_PATTERN:
            if char == '-':
                ble_id += '-'
                continue
            ble_id += unique[0]
            unique = unique[1:]
        return ble_id

    @staticmethod
    def __get_hextimestamp():
        timestamp = datetime.datetime.now(datetime.timezone.utc).timestamp()
        full_int_timestamp = int(timestamp * BLEIdGenerator.TIMESTAMP_MULTIPLIER)
        return BLEIdGenerator.__to_hex_str(full_int_timestamp)

    @staticmethod
    def __get_random_id(size):
        hex_chars = [BLEIdGenerator.__to_hex_str(x) for x in range(0, 16)]
        result = ''
        for x in range(size):
            result += random.choice(hex_chars)
        return result

    @staticmethod
    def __generate_unique_id(size) -> str:
        hex_time_id = BLEIdGenerator.__get_hextimestamp()
        random_id = BLEIdGenerator.__get_random_id(size - len(hex_time_id))
        result_id = hex_time_id + random_id
        return result_id[:size]

    @staticmethod
    def __to_hex_str(value: int):
        # [2:] para quitar el 0x luego de convertirlo
        return str(hex(value))[2:]
