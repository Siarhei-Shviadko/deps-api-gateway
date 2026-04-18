__all__ = ["EventRelayService"]

from typing import AsyncGenerator

from .iproxies import IEventRelayProxy


class EventRelayService:
    def __init__(self, event_relay_proxy: IEventRelayProxy):
        self._event_relay_proxy = event_relay_proxy

    async def subscribe(self) -> AsyncGenerator[bytes, None]:
        proxy_stream = self._event_relay_proxy.subscribe()
        async for event in proxy_stream:
            yield event
