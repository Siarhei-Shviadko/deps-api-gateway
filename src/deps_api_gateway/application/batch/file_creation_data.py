from typing import Optional, TypedDict

__all__ = ["ProcessingParametersDict", "FileCreationData"]


class ProcessingParametersDict(TypedDict):
    engine: Optional[str]
    language: Optional[str]
    llm_type: Optional[str]
    parsing_features: Optional[list[str]]


class FileCreationData(TypedDict):
    name: str
    path: str
    processing_params: ProcessingParametersDict
    document_type_id: Optional[str]
