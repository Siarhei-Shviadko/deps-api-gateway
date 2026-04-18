from typing import Any, Optional

from pydantic import Field

from ..ai_fusion import SerializedConversationInfo
from ..output_exporting import SerializedOutput
from ..validation import SerializedValidationResult
from .serialized_document import SerializedDocument

__all__ = ["DocumentDetailResponse"]


class DocumentDetailResponse(SerializedDocument):
    outputs: Optional[list[SerializedOutput]]
    conversation: Optional[SerializedConversationInfo]
    validation_results: Optional[SerializedValidationResult] = Field(..., alias="validationResults")
    metadata: Optional[dict[str, Any]]
