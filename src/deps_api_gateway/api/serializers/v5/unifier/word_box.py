from typing import Optional

from ...base import ConfiguredBaseModel
from .bbox import SerializedBbox
from .word import SerializedWord

__all__ = ["SerializedWordBox"]


class SerializedWordBox(ConfiguredBaseModel):
    word: SerializedWord
    bbox: Optional[SerializedBbox]
