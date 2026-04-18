from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel
from .extra_data import SerializedExtraData

__all__ = ["SaveSupplementRequest"]


class SaveSupplementRequest(ConfiguredBaseModel):
    data: list[SerializedExtraData]
    document_type_id: Optional[str] = Field(None, alias="documentTypeId")

    def get_raw_data(self):
        return [extra_data_element.model_dump(by_alias=False) for extra_data_element in self.data]
