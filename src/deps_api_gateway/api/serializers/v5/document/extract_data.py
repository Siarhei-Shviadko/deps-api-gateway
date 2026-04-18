from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["ExtractDataRequest"]


class ExtractDataRequest(ConfiguredBaseModel):
    document_ids: list[str] = Field(..., alias="documentIds", min_length=1)
    engine: str = Field(None, alias="engineName")
