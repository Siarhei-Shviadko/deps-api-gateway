from dataclasses import dataclass
from typing import Optional

from deps_api_gateway.constants import ImportSource

__all__ = ["ImportDocumentsData"]


@dataclass
class ImportDocumentsData:
    paths: list[str]
    source: ImportSource
    document_type_id: Optional[str] = None
    engine: Optional[str] = None
    language: Optional[str] = None
    invoke_unifier: Optional[bool] = None
    invoke_extraction: Optional[bool] = None
    assign_to_me: bool = None
    parsing_features: Optional[list[str]] = None
