from typing import AsyncGenerator, Protocol

__all__ = ["IEventRelayProxy"]


class IEventRelayProxy(Protocol):
    async def subscribe(self) -> AsyncGenerator[bytes, None]:
        ...
