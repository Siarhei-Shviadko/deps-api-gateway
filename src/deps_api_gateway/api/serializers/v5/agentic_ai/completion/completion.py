from datetime import datetime

from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["CompletionSerializer"]


class QuestionSerializer(ConfiguredBaseModel):
    text: str
    created_at: datetime = Field(alias="createdAt")


class ExecutionContextSerializer(ConfiguredBaseModel):
    text: str


class AnswerSerializer(ConfiguredBaseModel):
    text: str
    created_at: datetime = Field(alias="createdAt")


class CompletionSerializer(ConfiguredBaseModel):
    id: str
    question: QuestionSerializer
    execution_context: list[ExecutionContextSerializer] = Field(default_factory=list, alias="executionContext")
    answer: AnswerSerializer | None = None
