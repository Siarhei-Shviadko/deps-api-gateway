from typing import Optional

from pydantic import Field

from .....base import ConfiguredBaseModel

__all__ = ["SerializedBlurring", "SerializedThresholding", "SerializedTransformations"]


class SerializedBlurring(ConfiguredBaseModel):
    kernel: list[int]
    sigma: float


class SerializedThresholding(ConfiguredBaseModel):
    low_value: int = Field(..., alias="lowValue")
    high_value: int = Field(..., alias="highValue")
    flag: int


class SerializedTransformations(ConfiguredBaseModel):
    thresholding: Optional[SerializedThresholding] = None
    blurring: Optional[SerializedBlurring] = None
    grayscaling: bool = False
    orientation: Optional[str] = None
    angle: Optional[float] = None
