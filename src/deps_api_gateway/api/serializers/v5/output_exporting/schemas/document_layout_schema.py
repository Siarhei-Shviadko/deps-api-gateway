from enum import Enum

from ....base import ConfiguredBaseModel

__all__ = ["DocumentLayoutSchema"]


class ParsingFeature(str, Enum):
    TABLES = "tables"
    KEY_VALUE_PAIRS = "kvps"
    TEXT = "text"


class ParsingType(str, Enum):
    GCP_VISION = "GCP_VISION"
    AWS_TEXTRACT = "AWS_TEXTRACT"
    AZURE_FORM_RECOGNIZER = "AZURE_FORM_RECOGNIZER"

    TESSERACT = "TESSERACT"
    ABBYY = "ABBYY"
    CRAFT_TESSERACT = "CRAFT_TESSERACT"
    EASYOCR = "EASYOCR"
    PADDLEOCR = "PADDLEOCR"

    CUSTOM = "CUSTOM"


class DocumentLayoutSchema(ConfiguredBaseModel):
    parsing_type: ParsingType
    features: list[ParsingFeature]
