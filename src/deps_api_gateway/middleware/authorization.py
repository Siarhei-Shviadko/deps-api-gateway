import json
import os
from http import HTTPStatus
from typing import Any, Dict, List

import requests
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from deps_api_gateway.constants import (
    DEPS_TOKEN_HEADER_NAME,
    IAM_BASE_API_PREFIX,
    V2_PREFIX,
)
from deps_api_gateway.domain.exceptions import AuthorizationError


class AuthorizationMiddleware:
    def __init__(self, app: ASGIApp, iam_url: str):
        self.app = app
        self.iam_url = iam_url

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if self._is_authorization_not_required(os.path.basename(scope["path"])):
            await self.app(scope, receive, send)
            return

        headers = self._create_headers(scope)

        body_chunks: List[bytes] = []

        async def add_deps_token() -> Message:  # noqa: WPS430
            nonlocal body_chunks

            message = await receive()
            body = message.get("body", b"")
            body_chunks.append(body)

            if not message.get("more_body", False):
                body = b"".join(body_chunks)
                data = json.dumps(body.decode())
                authorization_response = self._authorize(headers=headers, data=data)

                if authorization_response.status_code != HTTPStatus.OK:
                    raise AuthorizationError

                scope["headers"].append(
                    (
                        bytes(DEPS_TOKEN_HEADER_NAME, "utf-8"),
                        bytes(authorization_response.headers["deps-token"], "utf-8"),
                    )
                )

            return message

        await self.app(scope, add_deps_token, send)

    def _authorize(self, headers: Dict[str, Any], data: str) -> requests.Response:
        authorization_url = f"{self.iam_url}{IAM_BASE_API_PREFIX}{V2_PREFIX}/authorize"

        return requests.post(authorization_url, headers=headers, data=data)

    def _create_headers(self, scope: Scope) -> Dict[str, Any]:
        headers = dict(scope["headers"])
        headers.update({"x-original-method": scope["method"]})
        headers.update({"x-original-path": scope["path"]})
        headers.update({"x-original-query": scope.get("query_string", "")})
        return headers

    def _is_authorization_not_required(self, basename: str) -> bool:
        return basename in ("docs", "openapi.json")  # noqa: WPS510
