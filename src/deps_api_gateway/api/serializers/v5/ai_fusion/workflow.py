from typing import Annotated

from pydantic import Field, StringConstraints

from deps_api_gateway.application.types import (
    RawLLMExecutionNode,
    RawLLMWorkflow,
    RawSequentialEdge,
)

from ...base import ConfiguredBaseModel

__all__ = ["SerializedLLMWorkflow"]


class SerializedLLMExecutionNode(ConfiguredBaseModel):
    id: str
    name: str
    prompt: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]

    def to_dict(self) -> RawLLMExecutionNode:
        return RawLLMExecutionNode(
            id=self.id,
            name=self.name,
            prompt=self.prompt,
        )


class SerializedSequentialEdge(ConfiguredBaseModel):
    source_id: str = Field(..., alias="sourceId")
    target_id: str = Field(..., alias="targetId")

    def to_dict(self) -> RawSequentialEdge:
        return RawSequentialEdge(
            source_id=self.source_id,
            target_id=self.target_id,
        )


class SerializedLLMWorkflow(ConfiguredBaseModel):
    start_node_id: str = Field(..., alias="startNodeId")
    end_node_id: str = Field(..., alias="endNodeId")
    nodes: list[SerializedLLMExecutionNode]
    edges: list[SerializedSequentialEdge]

    def to_dict(self) -> RawLLMWorkflow:
        return RawLLMWorkflow(
            start_node_id=self.start_node_id,
            end_node_id=self.end_node_id,
            nodes=[node.to_dict() for node in self.nodes],
            edges=[edge.to_dict() for edge in self.edges],
        )
