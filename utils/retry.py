import time
from functools import wraps
from typing import Callable, Type, Tuple, Any

RETRYABLE_EXCEPTIONS: Tuple[Type[BaseException], ...] = (
    ConnectionError,
    TimeoutError,
    RuntimeError,
    ValueError,
)


def retry(max_attempts: int = 3, delay_seconds: int = 3, exceptions: Tuple[Type[BaseException], ...] = RETRYABLE_EXCEPTIONS):
    def wrapper(fn: Callable[..., Any]):
        @wraps(fn)
        def inner(*args, **kwargs):
            attempt = 0
            last_exception = None
            while attempt < max_attempts:
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    attempt += 1
                    if attempt >= max_attempts:
                        raise
                    time.sleep(delay_seconds)
            raise last_exception
        return inner
    return wrapper
