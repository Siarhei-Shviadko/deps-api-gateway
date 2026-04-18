from ...proxy_response import ProxyResponse

__all__ = ["OCRConsolidator"]


class OCRConsolidator:
    @staticmethod
    def get_languages_from(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        return response.with_updated_content(
            status_code=response.status_code, content={"languages": response.json()}, headers=response.headers
        )

    @staticmethod
    def get_engines_from(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        return response.with_updated_content(
            status_code=response.status_code, content={"engines": response.json()}, headers=response.headers
        )

    @staticmethod
    def extract_text_from(response: ProxyResponse) -> ProxyResponse:
        if not response.is_ok():
            return response

        return response.with_updated_content(
            status_code=response.status_code, content={"textLines": response.json()}, headers=response.headers
        )
