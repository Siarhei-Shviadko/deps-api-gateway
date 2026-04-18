from http import HTTPStatus
from typing import Any, Optional

from ..proxy_response import ProxyResponse

__all__ = ["DocumentConsolidator"]


class DocumentConsolidator:
    @staticmethod
    def consolidate_document_detail(
        document_detail_response: ProxyResponse,
        output_exporting_response: Optional[ProxyResponse],
        ai_fusion_response: Optional[ProxyResponse],
        high_sparrow_response: Optional[ProxyResponse],
        document_metadata_response: Optional[ProxyResponse],
        parsing_response: Optional[ProxyResponse],
    ) -> ProxyResponse:
        failed_request = DocumentConsolidator._validate_document_detail_responses(
            document_detail_response=document_detail_response,
            output_exporting_response=output_exporting_response,
            ai_fusion_response=ai_fusion_response,
            high_sparrow_response=high_sparrow_response,
            document_metadata_response=document_metadata_response,
            parsing_response=parsing_response,
        )

        if failed_request is not None:
            return failed_request

        content = DocumentConsolidator._enrich_document_detail(
            document_detail_response=document_detail_response,
            output_exporting_response=output_exporting_response,
            ai_fusion_response=ai_fusion_response,
            high_sparrow_response=high_sparrow_response,
            document_metadata_response=document_metadata_response,
            parsing_response=parsing_response,
        )

        return document_detail_response.with_updated_content(
            status_code=document_detail_response.status_code, content=content, headers=document_detail_response.headers
        )

    @staticmethod
    def consolidate_delete_document_list(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        return response.without_content(status_code=HTTPStatus.NO_CONTENT, headers=response.headers)

    @staticmethod
    def consolidate_labels(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        return response.with_updated_content(
            status_code=response.status_code, content={"labels": response.json()}, headers=response.headers
        )

    @staticmethod
    def consolidate_add_label_response(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        return response.with_updated_content(
            status_code=response.status_code, content=response.json()[0], headers=response.headers  # type: ignore
        )

    @staticmethod
    def consolidate_add_label_batch_response(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        return response.with_updated_content(
            status_code=response.status_code, content={"result": response.json()}, headers=response.headers  # type: ignore
        )

    @staticmethod
    def consolidate_remove_label_response(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        return response.without_content(status_code=HTTPStatus.NO_CONTENT, headers=response.headers)

    @staticmethod
    def consolidate_states(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        states = [
            {
                "name": state["name"],
                "title": state["title"],
            }
            for state in response.json().values()  # type: ignore
        ]

        return response.with_updated_content(
            status_code=response.status_code, content={"states": states}, headers=response.headers
        )

    @staticmethod
    def consolidate_assigning_type(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        return response.with_updated_content(
            status_code=response.status_code, content=response.json()[0], headers=response.headers  # type: ignore
        )

    @staticmethod
    def _validate_document_detail_responses(
        document_detail_response: ProxyResponse,
        output_exporting_response: Optional[ProxyResponse],
        ai_fusion_response: Optional[ProxyResponse],
        high_sparrow_response: Optional[ProxyResponse],
        document_metadata_response: Optional[ProxyResponse],
        parsing_response: Optional[ProxyResponse],
    ) -> Optional[ProxyResponse]:
        if not document_detail_response.is_ok():
            return document_detail_response

        for response in (
            output_exporting_response,
            ai_fusion_response,
            high_sparrow_response,
            document_metadata_response,
            parsing_response,
        ):
            if response is not None and DocumentConsolidator._extra_response_invalid(response):
                return response

        return None

    @staticmethod
    def _enrich_document_detail(
        document_detail_response: ProxyResponse,
        output_exporting_response: Optional[ProxyResponse],
        ai_fusion_response: Optional[ProxyResponse],
        high_sparrow_response: Optional[ProxyResponse],
        document_metadata_response: Optional[ProxyResponse],
        parsing_response: Optional[ProxyResponse],
    ) -> dict:
        document_detail: dict[str, Any] = document_detail_response.json()  # type: ignore

        document_detail.update(
            {
                "outputs": (
                    output_exporting_response.json()["outputs"]  # type: ignore
                    if output_exporting_response is not None and not output_exporting_response.is_not_found()
                    else None
                ),
                "conversation": (
                    ai_fusion_response.json()
                    if ai_fusion_response is not None and not ai_fusion_response.is_not_found()
                    else None
                ),
                "validationResults": (
                    high_sparrow_response.json()
                    if high_sparrow_response is not None and not high_sparrow_response.is_not_found()
                    else None
                ),
                "metadata": (
                    document_metadata_response.json()["metadata"]  # type: ignore
                    if document_metadata_response is not None and not document_metadata_response.is_not_found()
                    else None
                ),
                "parsingInfo": parsing_response.json() if parsing_response is not None else None,
            }
        )

        return document_detail

    @staticmethod
    def _extra_response_invalid(response: ProxyResponse) -> bool:
        return not (response.is_ok() or response.is_not_found())
