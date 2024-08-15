#!/usr/bin/env python3

"""
A simple python script that stores data in Redis
"""

import redis
import uuid
import typing
import functools


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.

    Args:
        method (Callable): The method to replay the call history for.
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


def call_history(method):
    """
    A decorator to store the history of inputs and outputs
    for a particular function
    """
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        wrapper._redis.rpush(input_key, str(args))
        output = method(*args, **kwargs)
        wrapper._redis.rpush(output_key, str(output))
        return output
    return wrapper


class Cache:
    """
    A simple Redis cache that stores key-value pairs
    """

    def __init__(self):
        self._redis = redis.Redis()
        self.redis.flushdb()

    @call_history
    def store(data: typing.Union[str, bytes, int, float]) -> str:
        """A method to store data in Redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(key: str, fn: typing.Optional[typing.Callable] = None) ->
    typing.Union[str, bytes, int, float]:
        """A method to get data from Redis"""
        def get_str(key: str) -> str:
            """A method to get data from Redis"""
            return self._redis.get(key).decode('utf-8')

        def get_int(key: str) -> int:
            """A method to get data from Redis"""
            return int(self._redis.get(key).decode('utf-8'))

        if fn == int:
            return get_int(key)
        return get_str(key)
