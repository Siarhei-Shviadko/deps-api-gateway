from deps_api_gateway.application.types import TableFieldUpdateData

from ...base import ConfiguredBaseModel
from .field_data import SerializedTableCell

__all__ = ["TableFieldChunk"]


class TableFieldChunk(ConfiguredBaseModel):
    cells: list[SerializedTableCell]

    def to_dto(self) -> TableFieldUpdateData:
        return TableFieldUpdateData(**self.model_dump(by_alias=True, exclude_unset=True))
