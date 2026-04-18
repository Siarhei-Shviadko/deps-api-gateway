from ....base import ConfiguredBaseModel
from ..paginated_metadata import PaginatedMetadataSerializer
from .completion import CompletionSerializer

__all__ = ["CompletionsResponse"]


class CompletionsResponse(ConfiguredBaseModel):
    completions: list[CompletionSerializer]
    metadata: PaginatedMetadataSerializer
