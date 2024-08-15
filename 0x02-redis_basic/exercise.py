#!/usr/bin/env python3

"""
A simple python script that stores data in Redis
"""

import redis
import uuid
from typing import Optional, Callable, Union
from functools import wraps


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    """
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    redis_client = method.__self__._redis

    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_, output in zip(inputs, outputs):
        print(
            f"{method.__qualname__}(*{input_.decode('utf-8')}) "
            f"-> {output.decode('utf-8')}"
        )


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.
    """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Generate the key using the method's qualified name

        # Increment the count for this key
        self._redis.incr(key)

        # Call the original method and return its value
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a
    function in Redis.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_str = str(args)

        self._redis.rpush(method.__qualname__ + ":inputs", input_str)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


class Cache:
    """
    A simple Redis cache that stores key-value pairs
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """A method to store data in Redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """A method to get data from Redis"""
        def get_str(key: str) -> str:
            """A method to get data from Redis"""
            output = self._redis.get(key)
            if output is not None:
                return output.decode('utf-8')
            else:
                return None

        def get_int(key: str) -> int:
            """A method to get data from Redis"""
            output = self._redis.get(key)
            if output is not None:
                return int(output.decode('utf-8'))
            else:
                return None

        if fn == int:
            return get_int(key)
        return get_str(key)
