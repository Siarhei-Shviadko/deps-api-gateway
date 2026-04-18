from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["AddLabelOnDocumentRequest"]


class AddLabelOnDocumentRequest(ConfiguredBaseModel):
    label_id: str = Field(alias="labelId")
