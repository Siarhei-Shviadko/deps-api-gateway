from typing import Any

from .prompter_proxy import IPrompter

__all__ = ["PrompterService"]


class PrompterService:
    def __init__(self, prompter_proxy: IPrompter):
        self._prompter_proxy = prompter_proxy

    async def get_llms_with_codes(self) -> dict[str, Any]:
        return await self._prompter_proxy.get_llms_with_codes()
