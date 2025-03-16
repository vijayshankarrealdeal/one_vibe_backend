import uuid
import re
import random
from database_connect import redis_client

def generate_uuid():
    return str(uuid.uuid4())

def sanitize_filename(filename):
    """Removes or replaces unsafe characters from filenames."""
    return re.sub(r'[|<>:"/\\?*]', '_', filename) 


def generate_otp():
    return random.randint(100000,999999)

def is_rate_limiter(email):
    key = f"rate_limit:{email}"
    attempts = redis_client.get(key)
    if attempts and int(attempts) > 5:
        return True
    
    redis_client.incr(key)
    redis_client.expire(key, 60)
    return False

def track_fail_attemps(email):
    key = f"failed_attemps:{email}"
    attempts = redis_client.incr(key)
    if attempts > 5:
        redis_client.expire(key, 900)
        return True
    redis_client.expire(key, 900)
    return False