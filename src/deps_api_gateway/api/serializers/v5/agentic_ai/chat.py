import json
from typing import Any

from fastapi import Query
from pydantic import Field

from deps_api_gateway.application import ArgumentData, ContextArguments
from deps_api_gateway.domain.exceptions import IllegalArgument

from ...base import ConfiguredBaseModel

__all__ = [
    "ArgumentDataSerializer",
    "ChatRequest",
]

MAX_ARGUMENTS_LENGTH = 10000


class ArgumentDataSerializer(ConfiguredBaseModel):
    parameter: str
    value: Any

    def to_dict(self) -> ArgumentData:
        return {"parameter": self.parameter, "value": self.value}


class ChatRequest(ConfiguredBaseModel):
    user_question: str = Field(..., alias="userQuestion")
    arguments: dict[str, dict[str, list[ArgumentDataSerializer]]] | None = Field(
        None,
        description="Nested structure: {toolSetCode: {toolCode: [{parameter, value}]}}",
    )

    def to_context_arguments(self) -> ContextArguments | None:
        if self.arguments is None:
            return None
        return {
            tool_set_code: {tool_code: [arg.to_dict() for arg in args] for tool_code, args in tool_args.items()}
            for tool_set_code, tool_args in self.arguments.items()
        }

    @classmethod
    def from_query_params(
        cls,
        user_question: str = Query(..., alias="userQuestion"),
        arguments: str = Query("{}", max_length=MAX_ARGUMENTS_LENGTH),
    ) -> "ChatRequest":
        try:
            parsed_arguments = json.loads(arguments) if arguments else None
        except json.JSONDecodeError:
            raise IllegalArgument("Invalid JSON format for arguments")
        return cls(userQuestion=user_question, arguments=parsed_arguments)
