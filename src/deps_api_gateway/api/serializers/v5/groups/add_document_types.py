from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["AddDocumentTypesRequest"]


class AddDocumentTypesRequest(ConfiguredBaseModel):
    document_type_ids: list[str] = Field(..., min_length=1, alias="documentTypeIds")
