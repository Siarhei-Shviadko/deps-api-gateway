import json
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Union

from multidict import CIMultiDictProxy

__all__ = ["ProxyResponse"]


AnyJSONType = Union[dict, list, str, int, float, bool, None]


@dataclass
class ProxyResponse:
    status_code: int
    content: bytes
    headers: CIMultiDictProxy[str]

    def is_ok(self) -> bool:
        return HTTPStatus.OK <= self.status_code < HTTPStatus.MULTIPLE_CHOICES  # 200 <= ... < 300

    def is_not_found(self) -> bool:
        return self.status_code == HTTPStatus.NOT_FOUND

    def json(self) -> AnyJSONType:
        return json.loads(self.content)

    @classmethod
    def with_updated_content(
        cls, status_code: int, content: dict[str, Any], headers: CIMultiDictProxy[str]
    ) -> "ProxyResponse":
        updated_content = json.dumps(content).encode()

        updated_headers = headers.copy()
        updated_headers["content-length"] = str(len(updated_content))

        return cls(status_code, updated_content, CIMultiDictProxy(updated_headers))

    @classmethod
    def without_content(cls, status_code: int, headers: CIMultiDictProxy[str]) -> "ProxyResponse":
        updated_headers = headers.copy()
        updated_headers.pop("content-length", None)

        return cls(status_code, b"", CIMultiDictProxy(updated_headers))
