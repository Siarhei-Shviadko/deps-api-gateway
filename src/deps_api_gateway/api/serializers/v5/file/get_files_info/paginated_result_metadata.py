from ....base import ConfiguredBaseModel

__all__ = [
    "PaginatedResultMetadata",
]


class PaginatedResultMetadata(ConfiguredBaseModel):
    size: int
    total: int
