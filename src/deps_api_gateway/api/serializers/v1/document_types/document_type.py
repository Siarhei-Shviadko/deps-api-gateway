from datetime import datetime
from typing import Any, Optional

from pydantic import Field

from deps_api_gateway.application.types import FieldType

from ...base import ConfiguredBaseModel

__all__ = [
    "UpdateDocumentTypeLLMRequest",
    "CreateExtractionFieldRequest",
    "CreateDocumentTypeRequest",
    "DocumentTypesResponseData",
    "FieldResponseData",
    "DocumentTypeResponseData",
    "UpdateExtractionFieldRequest",
]


class UpdateDocumentTypeLLMRequest(ConfiguredBaseModel):
    llm_type: str = Field(alias="llmType", min_length=3, max_length=100)


class CreateDocumentTypeRequest(ConfiguredBaseModel):
    name: str
    description: Optional[str] = Field(None, max_length=100)


class CreateExtractionFieldRequest(ConfiguredBaseModel):
    name: str
    type: FieldType
    required: bool
    read_only: bool = Field(default=False, alias="readOnly")
    confidential: bool = Field(default=False)
    order: Optional[int] = Field(default=0)
    description: Optional[dict[str, Any]] = Field(default=None)
    extractor_id: Optional[str] = Field(default=None, alias="extractorId")
    field_code: Optional[str] = Field(default=None, alias="code")


class UpdateExtractionFieldRequest(ConfiguredBaseModel):
    name: Optional[str]
    required: Optional[bool]
    read_only: Optional[bool] = Field(default=None, alias="readOnly")
    confidential: Optional[bool] = None
    order: Optional[int] = Field(default=0)
    description: Optional[dict[str, Any]] = None
    extractor_id: Optional[str] = Field(default=None, alias="extractorId")


class FieldResponseData(ConfiguredBaseModel):
    code: str
    name: str
    required: bool = False
    type: str = Field(..., alias="fieldType")
    document_type_id: Optional[str] = Field(None, alias="documentTypeCode")
    id: Optional[str] = Field(None, alias="pk")
    order: Optional[int] = 0
    field_data: Optional[dict[str, Any]] = Field(None, alias="fieldMeta")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    confidential: bool = Field(default=False, alias="confidential")
    read_only: bool = Field(default=False, alias="readOnly")

    @classmethod
    def from_response(cls, field: dict[str, Any]) -> "FieldResponseData":
        return cls(
            code=field["code"],
            name=field["name"],
            required=field["required"],
            type=field.get("type") or field.get("fieldType"),
            document_type_id=field.get("documentTypeCode"),
            id=field.get("pk"),
            order=field.get("order"),
            field_data=field.get("fieldMeta"),
            created_at=field.get("createdAt"),
            confidential=field.get("confidential"),
            read_only=field.get("readOnly"),
        )


class DocumentTypeResponseData(ConfiguredBaseModel):
    id: str
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    tenant_id: str = Field(alias="tenantId")
    document_type: str = Field(alias="documentType")
    extraction_type: Optional[str] = Field(None, alias="extractionType")
    fields: Optional[list[FieldResponseData]] = None
    engine: Optional[str] = None
    language: Optional[str] = None
    description: Optional[str] = None
    llm_type: Optional[str] = Field(None, alias="llmType")

    @classmethod
    def from_response(cls, document_type: dict[str, Any]) -> "DocumentTypeResponseData":
        return cls(
            id=document_type["id"],
            created_at=document_type.get("createdAt"),
            tenant_id=document_type["tenantId"],
            document_type=document_type["documentType"],
            extraction_type=document_type.get("extractionType"),
            fields=[FieldResponseData.from_response(field) for field in document_type.get("fields") or []],
            engine=document_type.get("engine"),
            language=document_type.get("language"),
            description=document_type.get("description"),
            llm_type=document_type.get("llmType"),
        )


class DocumentTypesResponseData(ConfiguredBaseModel):
    result: list[DocumentTypeResponseData]  # noqa: WPS110

    @classmethod
    def from_response(cls, document_types: list[dict[str, Any]]) -> "DocumentTypesResponseData":
        return cls(
            result=[DocumentTypeResponseData.from_response(document_type) for document_type in document_types],
        )
