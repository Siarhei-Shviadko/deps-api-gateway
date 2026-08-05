from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = [
    "SerializedParagraphContent",
    "SerializedListContent",
    "SerializedTableContent",
    "SerializedImageContent",
]


class SerializedParagraphContent(ConfiguredBaseModel):
    markdown: str


class SerializedListContent(ConfiguredBaseModel):
    items: list[str]  # noqa: WPS110
    markdown: str


class SerializedTableContent(ConfiguredBaseModel):
    markdown_table: str = Field(..., alias="markdownTable")
    rows: int
    columns: int


class SerializedImageContent(ConfiguredBaseModel):
    name: str
    data: str
