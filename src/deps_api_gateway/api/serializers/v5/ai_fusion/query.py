from pydantic import Field

from deps_api_gateway.application.types import Cardinality, DataType, RawDataShape

from ...base import ConfiguredBaseModel
from .workflow import SerializedLLMWorkflow

__all__ = ["SerializedExtractionQuery", "MoveQueriesRequest"]


class SerializedDataShape(ConfiguredBaseModel):
    data_type: DataType = Field(default=DataType.STRING, alias="dataType")
    cardinality: Cardinality
    include_aliases: bool = Field(..., alias="includeAliases")

    def to_dict(self) -> RawDataShape:
        return RawDataShape(
            data_type=self.data_type,
            cardinality=self.cardinality,
            include_aliases=self.include_aliases,
        )


class SerializedExtractionQuery(ConfiguredBaseModel):
    code: str
    workflow: SerializedLLMWorkflow
    shape: SerializedDataShape


class MoveQueriesRequest(ConfiguredBaseModel):
    source_extractor_id: str = Field(..., alias="sourceExtractorId")
    target_extractor_id: str = Field(..., alias="targetExtractorId")
    fields_codes: list[str] = Field(..., alias="fieldsCodes", min_length=1)
