from typing import Optional

from pydantic import Field

from deps_api_gateway.application import LayoutState

from ...base import ConfiguredBaseModel

__all__ = ["SerializedReferenceLayout", "GetReferenceLayoutsResponse", "CreateReferenceLayoutResponse"]


class SerializedReferenceLayout(ConfiguredBaseModel):
    id: str
    prototype_id: str = Field(..., alias="prototypeId")
    title: Optional[str]
    state: LayoutState
    blob_name: str = Field(..., alias="blobName")


class GetReferenceLayoutsResponse(ConfiguredBaseModel):
    reference_layouts: list[SerializedReferenceLayout]


class CreateReferenceLayoutResponse(ConfiguredBaseModel):
    id: str
