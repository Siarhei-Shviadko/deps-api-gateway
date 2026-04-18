from typing import Optional

from pydantic import Field

from deps_api_gateway.constants import ImportSource
from deps_api_gateway.domain.dtos import ImportDocumentsData

from ...base import ConfiguredBaseModel

__all__ = ["ImportDocumentsRequest"]


class ImportDocumentsRequest(ConfiguredBaseModel):
    paths: list[str]
    source: ImportSource
    document_type_id: Optional[str] = Field(alias="documentType")
    engine: Optional[str] = None
    language: Optional[str] = None
    invoke_unifier: Optional[bool] = Field(default=True, alias="invokeUnifier")
    invoke_extraction: Optional[bool] = Field(default=True, alias="invokeExtraction")
    assign_to_me: bool = Field(alias="assignedToMe")
    parsing_features: Optional[list[str]] = Field(alias="parsingFeatures")

    def to_dto(self) -> ImportDocumentsData:
        return ImportDocumentsData(
            paths=self.paths,
            source=self.source,
            document_type_id=self.document_type_id,
            engine=self.engine,
            language=self.language,
            invoke_unifier=self.invoke_unifier,
            invoke_extraction=self.invoke_extraction,
            assign_to_me=self.assign_to_me,
            parsing_features=self.parsing_features,
        )
