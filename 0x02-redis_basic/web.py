import requests
import redis
import functools


def cache(key_prefix, expiration_time):
    """
    Decorator to cache the result of a function using Redis.

    Args:
        key_prefix (str): The prefix for the Redis key.
        expiration_time (int): The expiration time in seconds.

    Returns:
        Callable: The decorated function.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            redis_client = redis.Redis()
            key = f"{key_prefix}:{args[0]}"
            result = redis_client.get(key)
            if result is not None:
                return result.decode('utf-8')
            else:
                result = func(*args, **kwargs)
                redis_client.setex(key, expiration_time, result)
                return result
        return wrapper
    return decorator


@cache("count", 10)
def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    return requests.get(url).text
