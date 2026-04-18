from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["CreateLabelRequest"]


class CreateLabelRequest(ConfiguredBaseModel):
    label_name: str = Field(alias="labelName")
