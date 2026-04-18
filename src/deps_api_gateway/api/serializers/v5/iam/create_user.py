from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["CreateUserRequest"]


class CreateUserRequest(ConfiguredBaseModel):
    email: str
    username: Optional[str] = None
    first_name: Optional[str] = Field(default="", alias="firstName")
    last_name: Optional[str] = Field(default="", alias="lastName")
    organisation: Optional[str] = None
