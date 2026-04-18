from deps_api_gateway.application.document import DocumentState

from ...base import ConfiguredBaseModel

__all__ = ["GetStatesResponse"]


class StateInfo(ConfiguredBaseModel):
    name: DocumentState
    title: str


class GetStatesResponse(ConfiguredBaseModel):
    states: list[StateInfo]
