from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedBlobFile", "UpdateDocumentBlobFileData"]


class SerializedBlobFile(ConfiguredBaseModel):
    blob_name: str = Field(alias="blobName")
    url: Optional[str] = None


class UpdateDocumentBlobFileData(ConfiguredBaseModel):
    blob_name: str = Field(alias="blobName")
