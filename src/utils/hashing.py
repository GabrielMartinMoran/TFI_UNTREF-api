from hashlib import sha256


def hash_password(password: str) -> str:
    if not password:
        return None
    return sha256(password.encode('utf-8')).hexdigest()
