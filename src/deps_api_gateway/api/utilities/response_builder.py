from typing import Union

from fastapi.responses import JSONResponse, Response

from deps_api_gateway.constants import JSON_CONTENT_TYPE

AnyPossibleContent = Union[str, bytes, dict, list, None]

__all__ = ["ResponseBuilder"]


class ResponseBuilder:
    def __init__(self):
        self._content_type = JSON_CONTENT_TYPE
        self._response_payload = None
        self._status_code = 200
        self._headers = None

    def with_content(self, payload: AnyPossibleContent):
        self._response_payload = payload
        return self

    def with_status(self, status: int):
        self._status_code = status
        return self

    def with_content_type(self, content_type: str):
        self._content_type = content_type
        return self

    def with_headers(self, headers: dict):
        self._headers = headers
        return self

    def build(self) -> Response:
        if self._is_serializeable() and self._content_type == JSON_CONTENT_TYPE:
            return JSONResponse(content=self._response_payload, status_code=self._status_code, headers=self._headers)
        return Response(
            content=self._response_payload,
            status_code=self._status_code,
            media_type=self._content_type,
            headers=self._headers,
        )

    def _is_serializeable(self):
        return isinstance(self._response_payload, (dict, list))
