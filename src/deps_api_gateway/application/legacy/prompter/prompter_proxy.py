from typing import Any, Protocol

__all__ = ["IPrompter"]


class IPrompter(Protocol):
    async def get_llms_with_codes(self) -> dict[str, Any]:
        ...
