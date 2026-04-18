from typing import Optional

from pydantic import Field

from ......base import ConfiguredBaseModel
from ...point import SerializedPoint
from .barcode import SerializedBarcode
from .formula import SerializedFormula
from .selection_mark import SerializedSelectionMark
from .signature import SerializedSignature
from .word import SerializedWord

__all__ = ["SerializedLine"]


class SerializedLine(ConfiguredBaseModel):
    order: int
    content: str
    confidence: Optional[float] = None
    polygon: list[SerializedPoint]
    words: list[SerializedWord]
    selection_marks: list[SerializedSelectionMark] = Field(..., alias="selectionMarks")
    barcodes: list[SerializedBarcode]
    formulas: list[SerializedFormula]
    signatures: list[SerializedSignature]
