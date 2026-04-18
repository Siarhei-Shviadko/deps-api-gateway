from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["CreateAgentVendorRequest", "CreateAgentVendorResponse", "GetAgentVendorsResponse"]

MIN_NAME_LENGTH = 1


class CreateAgentVendorRequest(ConfiguredBaseModel):
    name: str = Field(..., min_length=MIN_NAME_LENGTH)
    description: str
    base_url: str = Field(..., alias="baseUrl")
    avatar_url: str | None = Field(None, alias="avatarUrl")


class CreateAgentVendorResponse(ConfiguredBaseModel):
    id: str


class ConnectionParameters(ConfiguredBaseModel):
    base_url: str = Field(..., alias="baseUrl")


class AgentVendor(ConfiguredBaseModel):
    id: str
    name: str
    description: str
    avatar_url: str | None = Field(..., alias="avatarUrl")
    connection_parameters: ConnectionParameters = Field(..., alias="connectionParameters")


class GetAgentVendorsResponse(ConfiguredBaseModel):
    agent_vendors: list[AgentVendor]
