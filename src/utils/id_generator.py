import datetime
import random
import hashlib
from bson import objectid

ID_LENGTH = 24


def generate_unique_id() -> str:
    generated_id = F'{datetime.datetime.now().timestamp()}{random.randint(100000000, 999999999)}'
    hashed_id = hashlib.sha1(generated_id.encode("UTF-8")).hexdigest()
    return str(objectid.ObjectId(hashed_id[:ID_LENGTH]))
