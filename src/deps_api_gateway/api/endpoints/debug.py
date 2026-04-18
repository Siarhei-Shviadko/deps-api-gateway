from fastapi import APIRouter, status

__all__ = ["debug_router"]
debug_router = APIRouter()


@debug_router.get("/debug/500", tags=["Debug"], status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
def raise_internal_server_error():
    raise ValueError()
