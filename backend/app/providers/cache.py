from datetime import datetime, timedelta

_cache = {}

CACHE_TIME = timedelta(hours=1)


def get(key):
    if key not in _cache:
        return None

    value, timestamp = _cache[key]

    if datetime.now() - timestamp > CACHE_TIME:
        del _cache[key]
        return None

    return value


def set(key, value):
    _cache[key] = (value, datetime.now())