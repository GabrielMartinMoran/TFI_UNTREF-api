import random
import hashlib

from src.common import dates


class IdGenerator:
    _ID_PATTERN = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    _TIMESTAMP_MULTIPLIER = 1000000

    @staticmethod
    def generate_id(key: str) -> str:
        key_bytes = key.encode('utf-8')
        hashed_key = hashlib.md5(key_bytes).hexdigest()
        return IdGenerator._format_hex_id(hashed_key)

    @staticmethod
    def generate_unique_id() -> str:
        chars_length = len(IdGenerator._ID_PATTERN.replace('-', ''))
        unique_id = IdGenerator._generate_unique_hash(chars_length)
        return IdGenerator._format_hex_id(unique_id)

    @staticmethod
    def _format_hex_id(hex_id: str) -> str:
        _hex_id = hex_id
        formatted = ''
        for char in IdGenerator._ID_PATTERN:
            if char == '-':
                formatted += '-'
                continue
            formatted += _hex_id[0]
            _hex_id = _hex_id[1:]
        return formatted

    @staticmethod
    def _get_hex_timestamp() -> str:
        timestamp = dates.now().timestamp()
        full_int_timestamp = int(timestamp * IdGenerator._TIMESTAMP_MULTIPLIER)
        return IdGenerator._int_to_hex_str(full_int_timestamp)

    @staticmethod
    def _get_random_id(size: int) -> str:
        hex_chars = [IdGenerator._int_to_hex_str(x) for x in range(0, 16)]
        result = ''
        for x in range(size):
            result += random.choice(hex_chars)
        return result

    @staticmethod
    def _generate_unique_hash(size: int) -> str:
        hex_time_id = IdGenerator._get_hex_timestamp()
        random_id = IdGenerator._get_random_id(size - len(hex_time_id))
        result_id = hex_time_id + random_id
        return result_id[:size]

    @staticmethod
    def _int_to_hex_str(value: int) -> str:
        # [2:] para quitar el 0x luego de convertirlo
        return str(hex(value))[2:]
