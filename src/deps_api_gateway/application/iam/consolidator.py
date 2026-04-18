from http import HTTPStatus

from ..proxy_response import ProxyResponse

__all__ = ["IAMConsolidator"]


class IAMConsolidator:
    @staticmethod
    def consolidate_organisations_list(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        content = {"organisations": response.json()}  # type: ignore

        return response.with_updated_content(
            status_code=response.status_code, content=content, headers=response.headers
        )

    @staticmethod
    def consolidate_deleting_organisation(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        return response.without_content(status_code=HTTPStatus.NO_CONTENT, headers=response.headers)
