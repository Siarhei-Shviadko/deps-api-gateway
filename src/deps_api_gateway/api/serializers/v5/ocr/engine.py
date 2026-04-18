from deps_api_gateway.application.tools import OCREngineEnum

from ...base import ConfiguredBaseModel

__all__ = ["SerializedOCREngine"]


class SerializedOCREngine(ConfiguredBaseModel):
    code: OCREngineEnum
    name: str
