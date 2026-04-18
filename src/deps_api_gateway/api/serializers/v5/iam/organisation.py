from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedOrganisation", "GetOrganisationsResponse", "SerializedInvitation"]


class SerializedOrganisation(ConfiguredBaseModel):
    pk: Optional[str]
    name: str
    customization_url: Optional[str] = Field(None, alias="customizationUrl")


class GetOrganisationsResponse(ConfiguredBaseModel):
    organisations: list[SerializedOrganisation]


class SerializedInvitation(ConfiguredBaseModel):
    email: str
