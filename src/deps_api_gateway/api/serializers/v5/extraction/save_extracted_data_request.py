from typing import Optional

from deps_api_gateway.application.types import SaveExtractedDataDTO

from ...base import ConfiguredBaseModel
from .extracted_field import SerializedExtractedField
from .group import SerializedGroup

__all__ = ["SaveExtractedDataRequest"]


class SaveExtractedDataRequest(ConfiguredBaseModel):
    fields: list[SerializedExtractedField]
    groups: Optional[list[SerializedGroup]] = None

    def to_dto(self) -> SaveExtractedDataDTO:
        return SaveExtractedDataDTO(**self.model_dump(by_alias=True, exclude_unset=True))
