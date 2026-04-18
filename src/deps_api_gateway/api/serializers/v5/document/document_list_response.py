from ...base import ConfiguredBaseModel
from .serialized_document import SerializedDocument

__all__ = ["DocumentListResponse", "DocumentListNoMetaResponse"]


class DocumentListMeta(ConfiguredBaseModel):
    total: int
    size: int


class DocumentListResponse(ConfiguredBaseModel):
    meta: DocumentListMeta
    result: list[SerializedDocument]


class DocumentListNoMetaResponse(ConfiguredBaseModel):
    result: list[SerializedDocument]
