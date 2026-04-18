from dataclasses import dataclass
from typing import Any, Optional

__all__ = ["ExtractionFieldData"]


@dataclass
class ExtractionFieldData:
    code: str
    name: Optional[str] = None
    description: Optional[dict[str, Any]] = None
    required: Optional[bool] = None
    read_only: Optional[bool] = None
    confidential: Optional[bool] = None
    order: Optional[int] = None
    extractor_id: Optional[str] = None
