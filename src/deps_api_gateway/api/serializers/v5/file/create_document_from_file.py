from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["CreateDocumentFromFileRequest"]


class CreateDocumentFromFileRequest(ConfiguredBaseModel):
    document_type_id: str = Field(..., alias="documentTypeId")
