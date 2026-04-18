from typing import Any, Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["CreateBatchFromFileRequest"]


class SerializedBatchFile(ConfiguredBaseModel):
    name: str = Field(..., min_length=1)
    path: str = Field(..., min_length=1)
    document_type_id: Optional[str] = Field(None, alias="documentTypeId")


class CreateBatchFromFileRequest(ConfiguredBaseModel):
    batch_name: str = Field(..., alias="batchName")
    files: list[SerializedBatchFile]
    group_id: str | None = Field(None, alias="groupId")

    @property
    def batch_files(self) -> list[dict[str, Any]]:
        return [bf.model_dump(by_alias=True) for bf in self.files]
