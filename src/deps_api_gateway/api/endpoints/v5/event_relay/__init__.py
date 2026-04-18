from fastapi import APIRouter

from .events import events_router

__all__ = ["event_relay_router"]

event_relay_router = APIRouter()
event_relay_router.include_router(events_router)
