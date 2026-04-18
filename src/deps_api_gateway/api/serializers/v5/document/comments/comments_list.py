from pydantic import Field

from ....base import ConfiguredBaseModel
from .comment import SerializedComment

__all__ = ["SerializedCommentsList"]


class SerializedCommentsList(ConfiguredBaseModel):
    comments: list[SerializedComment] = Field(default_factory=list)
