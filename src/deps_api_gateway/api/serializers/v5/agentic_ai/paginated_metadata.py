from ...base import ConfiguredBaseModel

__all__ = [
    "PaginatedMetadataSerializer",
]


class PaginatedMetadataSerializer(ConfiguredBaseModel):
    size: int
    total: int
