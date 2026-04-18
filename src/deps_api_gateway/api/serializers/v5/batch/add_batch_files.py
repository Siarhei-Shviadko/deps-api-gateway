from typing import Any

from pydantic import Field

from ...base import ConfiguredBaseModel
from .create_file_data import FileRequestSerializer

__all__ = ["AddBatchFilesRequest"]


class AddBatchFilesRequest(ConfiguredBaseModel):
    files: list[FileRequestSerializer] = Field(..., min_length=1)

    @property
    def files_as_dict(self) -> list[dict[str, Any]]:
        return [f.model_dump(by_alias=True) for f in self.files]
