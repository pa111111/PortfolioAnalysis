from functools import wraps
from hashlib import md5
from dogpile.cache import make_region
from dogpile.cache.api import NO_VALUE

cache_region = make_region().configure('dogpile.cache.memory', expiration_time=3600)


def cache_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = md5(str((func.__name__, args, kwargs)).encode('utf-8')).hexdigest()
        cached_result = cache_region.get(cache_key)
        if cached_result is not NO_VALUE:
            return cached_result
        result = func(*args, **kwargs)
        cache_region.set(cache_key, result)
        return result

    return wrapper
