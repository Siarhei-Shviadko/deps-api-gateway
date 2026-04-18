from typing import Any

from ..parsing import IParsingProxy, PageBatch, ParsingFeature, ParsingType

__all__ = ["ParsingService"]


class ParsingService:
    def __init__(self, parsing_proxy: IParsingProxy) -> None:
        self._parsing_proxy = parsing_proxy

    async def get_pages(
        self,
        document_layout_id: str,
        parsing_type: ParsingType,
        features: set[ParsingFeature],
        batch_index: int = PageBatch.index,
        batch_size: int = PageBatch.size,
    ) -> dict[str, Any]:
        return await self._parsing_proxy.get_pages(
            document_layout_id=document_layout_id,
            parsing_type=parsing_type,
            features=features,
            batch_index=batch_index,
            batch_size=batch_size,
        )
