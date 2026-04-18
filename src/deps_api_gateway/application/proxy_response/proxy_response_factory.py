from typing import Any

from .proxy_response import ProxyResponse

__all__ = ["ProxyResponseFactory"]


class ProxyResponseFactory:
    @staticmethod
    def make_response_from(response: dict[str, Any]) -> ProxyResponse:
        return ProxyResponse(
            status_code=response["status_code"],
            content=response["content"],
            headers=response["headers"],
        )
