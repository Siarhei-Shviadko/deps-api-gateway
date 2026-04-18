from typing import Optional

from pydantic import Field

from deps_api_gateway.application.document import DocumentState

from ...base import ConfiguredBaseModel

__all__ = ["SerializedError"]


class SerializedError(ConfiguredBaseModel):
    description: str = ""
    in_state: Optional[DocumentState] = Field(None, alias="inState")
