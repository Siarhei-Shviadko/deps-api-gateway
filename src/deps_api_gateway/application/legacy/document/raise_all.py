__all__ = ["raise_all"]


def raise_all(*exceptions: BaseException):
    if not exceptions:
        raise
    e, *exceptions = exceptions  # type: ignore
    try:
        raise e
    except Exception:
        raise e from raise_all(*exceptions)
