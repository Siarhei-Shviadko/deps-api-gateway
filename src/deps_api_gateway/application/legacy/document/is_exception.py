from typing import Any


def is_exception(value: Any):
    return isinstance(value, BaseException)
