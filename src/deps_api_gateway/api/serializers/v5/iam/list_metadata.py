from ...base import ConfiguredBaseModel

__all__ = ["ListMetadata"]


class ListMetadata(ConfiguredBaseModel):
    total: int
    size: int
