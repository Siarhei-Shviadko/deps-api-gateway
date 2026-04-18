from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from deps_api_gateway.application import EventRelayService
from deps_api_gateway.constants import EVENT_RELAY_ROUTER_PREFIX
from deps_api_gateway.containers import Application

__all__ = ["events_router"]

events_router = APIRouter(prefix=EVENT_RELAY_ROUTER_PREFIX, tags=["Server Sent Events"])


@events_router.get(
    "/stream",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    description="Subscribes to domain events of your tenant",
)
@inject
async def get_events(application: EventRelayService = Depends(Provide[Application.event_relay])) -> StreamingResponse:
    return StreamingResponse(
        application.subscribe(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
