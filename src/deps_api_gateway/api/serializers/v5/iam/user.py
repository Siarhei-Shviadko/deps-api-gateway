from datetime import datetime
from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel
from .organisation import SerializedOrganisation

__all__ = [
    "SerializedUser",
    "SerializedExpandedUser",
    "ApproveUserResponse",
    "DeclineUserRequest",
    "DeleteUserResponse",
]


class SerializedUser(ConfiguredBaseModel):
    pk: Optional[str]
    username: Optional[str]
    email: Optional[str]
    first_name: Optional[str] = Field("", alias="firstName")
    last_name: Optional[str] = Field("", alias="lastName")
    organisation: Optional[str]
    created_at: datetime = Field(..., alias="creationDate")


class SerializedExpandedUser(SerializedUser):
    organisation: Optional[SerializedOrganisation]
    default_customization_url: Optional[str] = Field(alias="defaultCustomizationUrl")


class ApproveUserResponse(ConfiguredBaseModel):
    approved_users: list[str] = Field(default_factory=list, alias="approvedUsers")


class DeclineUserRequest(ConfiguredBaseModel):
    declined_users: list[str] = Field(default_factory=list, alias="declinedUsers")


class DeleteUserResponse(ConfiguredBaseModel):
    deleted_users: list[str] = Field(default_factory=list, alias="deletedUsers")
