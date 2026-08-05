from typing import Any, Optional

from ..proxy_response import ProxyResponse

__all__ = ["GroupsConsolidator"]


class GroupsConsolidator:
    @classmethod
    def consolidate_groups(
        cls,
        groups_response: ProxyResponse,
        splittings_response: ProxyResponse,
    ) -> ProxyResponse:
        if not groups_response.is_ok():
            return groups_response

        if cls._extra_response_invalid(splittings_response):
            return splittings_response

        splitters: list[dict[str, Any]] = splittings_response.json()["splitters"]  # type: ignore
        splitter_by_group_id = {s["groupId"]: s for s in splitters if s.get("documentTypeId") is None}

        groups: dict[str, Any] = groups_response.json()  # type: ignore
        for group in groups["result"]:
            group["splitter"] = splitter_by_group_id.get(group["id"])

        return groups_response.with_updated_content(
            status_code=groups_response.status_code,
            content=groups,
            headers=groups_response.headers,
        )

    @classmethod
    def consolidate_group(
        cls,
        groups_response: ProxyResponse,
        classification_response: Optional[ProxyResponse],
        splitter_response: Optional[ProxyResponse],
    ) -> ProxyResponse:
        failed_request = cls._validate_get_group_responses(
            groups_response=groups_response,
            classification_response=classification_response,
            splitter_response=splitter_response,
        )

        if failed_request is not None:
            return failed_request

        content = cls._enrich_group(
            groups_response=groups_response,
            classification_response=classification_response,
            splitter_response=splitter_response,
        )

        return groups_response.with_updated_content(
            status_code=groups_response.status_code, content=content, headers=groups_response.headers
        )

    @classmethod
    def _validate_get_group_responses(
        cls,
        groups_response: ProxyResponse,
        classification_response: Optional[ProxyResponse],
        splitter_response: Optional[ProxyResponse],
    ) -> Optional[ProxyResponse]:
        if not groups_response.is_ok():
            return groups_response

        if classification_response is not None and cls._extra_response_invalid(classification_response):
            return classification_response

        if splitter_response is not None and cls._extra_response_invalid(splitter_response):
            return splitter_response

        return None

    @staticmethod
    def _enrich_group(
        groups_response: ProxyResponse,
        classification_response: Optional[ProxyResponse],
        splitter_response: Optional[ProxyResponse],
    ) -> dict[str, Any]:
        group: dict[str, Any] = groups_response.json()  # type: ignore

        group["group"]["genAiClassifiers"] = (
            None
            if classification_response is None or classification_response.is_not_found()
            else classification_response.json()["genAiClassifiers"]  # type: ignore
        )

        group["group"]["splitters"] = (
            None
            if splitter_response is None or splitter_response.is_not_found()
            else splitter_response.json()["splitters"]  # type: ignore
        )

        return group

    @staticmethod
    def _extra_response_invalid(response: ProxyResponse) -> bool:
        return not (response.is_ok() or response.is_not_found())
