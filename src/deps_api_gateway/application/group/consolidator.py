from typing import Any, Optional

from ..proxy_response import ProxyResponse

__all__ = ["GroupsConsolidator"]


class GroupsConsolidator:
    @classmethod
    def consolidate_group(
        cls,
        groups_response: ProxyResponse,
        classification_response: Optional[ProxyResponse],
    ) -> ProxyResponse:
        failed_request = cls._validate_get_group_responses(
            groups_response=groups_response,
            classification_response=classification_response,
        )

        if failed_request is not None:
            return failed_request

        content = cls._enrich_group(
            groups_response=groups_response,
            classification_response=classification_response,
        )

        return groups_response.with_updated_content(
            status_code=groups_response.status_code, content=content, headers=groups_response.headers
        )

    @classmethod
    def _validate_get_group_responses(
        cls,
        groups_response: ProxyResponse,
        classification_response: Optional[ProxyResponse],
    ) -> Optional[ProxyResponse]:
        if not groups_response.is_ok():
            return groups_response

        if classification_response is not None and cls._extra_response_invalid(classification_response):
            return classification_response

        return None

    @staticmethod
    def _enrich_group(
        groups_response: ProxyResponse,
        classification_response: Optional[ProxyResponse],
    ) -> dict[str, Any]:
        group: dict[str, Any] = groups_response.json()  # type: ignore

        group["group"]["genAiClassifiers"] = (
            None
            if classification_response is None or classification_response.is_not_found()
            else classification_response.json()["genAiClassifiers"]  # type: ignore
        )

        return group

    @staticmethod
    def _extra_response_invalid(response: ProxyResponse) -> bool:
        return not (response.is_ok() or response.is_not_found())
