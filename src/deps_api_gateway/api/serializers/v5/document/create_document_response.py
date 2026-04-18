from pydantic import BaseModel, ConfigDict, Field

__all__ = ["CreateDocumentResponse"]


class CreateDocumentResponse(BaseModel):
    document_id: str = Field(..., alias="id")

    model_config = ConfigDict(validate_by_name=True)
