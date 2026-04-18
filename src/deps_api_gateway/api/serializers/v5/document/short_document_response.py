from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["ShortDocumentResponse"]


class ShortDocumentResponse(ConfiguredBaseModel):
    pk: str = Field(..., alias="_id")
