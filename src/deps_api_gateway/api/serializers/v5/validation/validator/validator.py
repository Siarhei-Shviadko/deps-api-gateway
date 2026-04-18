from typing import Optional

from pydantic import Field

from ....base import ConfiguredBaseModel
from ..rule import SerializedRule
from .validator_type import ValidatorType

__all__ = ["SerializedValidator"]


class SerializedValidator(ConfiguredBaseModel):
    code: str
    type: ValidatorType
    is_required: bool = Field(alias="isRequired")
    rules: Optional[list[SerializedRule]]
