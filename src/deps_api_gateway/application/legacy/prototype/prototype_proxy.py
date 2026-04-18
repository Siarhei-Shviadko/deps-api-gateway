from typing import Any, Protocol

__all__ = ["ILegacyPrototypeProxy"]


class ILegacyPrototypeProxy(Protocol):
    async def find_layouts(self, prototype_id: str) -> dict[str, Any]:
        ...

    async def find_layout(self, prototype_id: str, layout_id: str) -> dict[str, Any]:
        ...

    async def delete_layout(self, prototype_id: str, layout_id: str) -> None:
        ...

    async def delete_layouts(self, prototype_id: str, layout_ids: list[str]) -> None:
        ...
