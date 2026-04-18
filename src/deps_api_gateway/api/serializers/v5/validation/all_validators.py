from pydantic import Field

from ...base import ConfiguredBaseModel
from .cross_field_validator import SerializedCrossFieldValidator
from .external_validator import SerializedExternalValidator
from .validator import SerializedValidator

__all__ = ["GetAllValidatorsResponse"]


class GetAllValidatorsResponse(ConfiguredBaseModel):
    validators: list[SerializedValidator]
    cross_field_validators: list[SerializedCrossFieldValidator] = Field(..., alias="crossFieldValidators")
    external_validators: list[SerializedExternalValidator] = Field(..., alias="externalValidators")
