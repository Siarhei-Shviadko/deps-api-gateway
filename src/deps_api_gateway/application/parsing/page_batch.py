from dataclasses import dataclass

__all__ = ["PageBatch"]

DEFAULT_BATCH_INDEX = 0
DEFAULT_BATCH_SIZE = 1


@dataclass
class PageBatch:
    index: int = DEFAULT_BATCH_INDEX
    size: int = DEFAULT_BATCH_SIZE
