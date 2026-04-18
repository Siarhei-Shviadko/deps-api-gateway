from typing import Any
from urllib.parse import urlencode

from deps_api_gateway.application import PageBatch, ParsingFeature, ParsingType
from deps_api_gateway.constants import API_PREFIX

__all__ = ["GetPageBatchUrlFactory"]


class GetPageBatchUrlFactory:
    def __init__(
        self,
        document_layout_id: str,
        parsing_type: ParsingType,
        features: set[ParsingFeature],
        batch_index: int = PageBatch.index,
        batch_size: int = PageBatch.size,
    ) -> None:
        self._document_layout_id = document_layout_id
        self._parsing_type = parsing_type
        self._features = features
        self._batch_index = batch_index
        self._batch_size = batch_size

    def params(self) -> dict[str, Any]:
        return {
            "features": [feature.value for feature in self._features],
            "parsingType": self._parsing_type.value,
            "batchSize": self._batch_size,
            "batchIndex": self._batch_index,
        }

    def next(self) -> str:
        params = self.params()
        params["batchIndex"] = self._batch_index + 1

        return f"{API_PREFIX}/document-layout/{self._document_layout_id}/pages?{urlencode(params, doseq=True)}"

    def previous(self) -> str:
        if self._batch_index <= 0:
            return ""

        params = self.params()
        params["batchIndex"] = self._batch_index - 1

        return f"{API_PREFIX}/document-layout/{self._document_layout_id}/pages?{urlencode(params, doseq=True)}"
