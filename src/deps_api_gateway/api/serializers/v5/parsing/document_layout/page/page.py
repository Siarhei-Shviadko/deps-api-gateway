from typing import Optional

from pydantic import Field

from .....base import ConfiguredBaseModel
from .dimension import SerializedDimension
from .group import SerializedGroup
from .image import SerializedImage
from .key_value_pair import SerializedKeyValuePair
from .language import SerializedLanguage
from .paragraph import SerializedParagraph
from .table import SerializedTable
from .transformations import SerializedTransformations

__all__ = ["SerializedPage"]


class SerializedPage(ConfiguredBaseModel):
    id: str
    page_number: int = Field(..., alias="pageNumber")
    parsing_type: str = Field(..., alias="parsingType")
    dimension: Optional[SerializedDimension] = None
    languages: Optional[list[SerializedLanguage]] = None
    file_path: Optional[str] = Field(None, alias="filePath")
    transformations: Optional[SerializedTransformations] = None

    images: list[SerializedImage]
    paragraphs: list[SerializedParagraph]
    tables: list[SerializedTable]
    key_value_pairs: list[SerializedKeyValuePair] = Field(..., alias="keyValuePairs")
    groups: list[SerializedGroup] = Field(default_factory=list)
