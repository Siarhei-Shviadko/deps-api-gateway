from ...proxy_response import ProxyResponse

__all__ = ["TemplateConsolidator"]


class TemplateConsolidator:
    @staticmethod
    def consolidate_template_versions(response: ProxyResponse):
        return ProxyResponse.with_updated_content(
            status_code=response.status_code,
            content={"versions": response.json()},
            headers=response.headers,
        )
