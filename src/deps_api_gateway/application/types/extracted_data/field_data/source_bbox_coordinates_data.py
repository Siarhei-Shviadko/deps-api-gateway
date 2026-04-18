from typing import TypedDict

from deps_api_gateway.application.types import Bbox

__all__ = ["SourceBboxCoordinatesData"]


class SourceBboxCoordinatesData(TypedDict):
    sourceId: str
    bboxes: list[Bbox]
