from typing import Any

from fastapi import APIRouter, Request
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import HTMLResponse

from deps_api_gateway.constants import (
    BASE_API_PREFIX,
    BASE_API_V1_PREFIX,
    BASE_API_V5_PREFIX,
    BASE_API_V6_PREFIX,
    SWAGGER_DOC_URL,
)

from ..utilities import add_security_to_openapi, build_openapi_schema

__all__ = ["docs_router"]


docs_router = APIRouter()


@docs_router.get(f"{BASE_API_V1_PREFIX}{SWAGGER_DOC_URL}", include_in_schema=False)
async def get_v1_docs(request: Request) -> HTMLResponse:
    return get_swagger_ui_html(openapi_url=f"{BASE_API_V1_PREFIX}/openapi.json", title=f"{request.app.title} v1")


@docs_router.get(f"{BASE_API_V5_PREFIX}{SWAGGER_DOC_URL}", include_in_schema=False)
async def get_v5_docs(request: Request) -> HTMLResponse:
    return get_swagger_ui_html(openapi_url=f"{BASE_API_V5_PREFIX}/openapi.json", title=f"{request.app.title} v5")


@docs_router.get(f"{BASE_API_V1_PREFIX}/openapi.json", include_in_schema=False)
async def get_v1_openapi(request: Request) -> dict[str, Any]:
    openapi_schema = build_openapi_schema(
        app=request.app,
        paths_filter=lambda key_value: key_value[0].startswith((BASE_API_V1_PREFIX, BASE_API_PREFIX)),
        title=f"{request.app.title} v1",
    )
    add_security_to_openapi(openapi_schema)

    return openapi_schema


@docs_router.get(f"{BASE_API_V5_PREFIX}/openapi.json", include_in_schema=False)
async def get_v5_openapi(request: Request) -> dict[str, Any]:
    openapi_schema = build_openapi_schema(
        app=request.app,
        paths_filter=lambda key_value: key_value[0].startswith(BASE_API_V5_PREFIX),
        title=f"{request.app.title} v5",
    )
    add_security_to_openapi(openapi_schema)

    return openapi_schema


@docs_router.get(f"{BASE_API_V6_PREFIX}{SWAGGER_DOC_URL}", include_in_schema=False)
async def get_v6_docs(request: Request) -> HTMLResponse:
    return get_swagger_ui_html(openapi_url=f"{BASE_API_V6_PREFIX}/openapi.json", title=f"{request.app.title} v6")


@docs_router.get(f"{BASE_API_V6_PREFIX}/openapi.json", include_in_schema=False)
async def get_v6_openapi(request: Request) -> dict[str, Any]:
    openapi_schema = build_openapi_schema(
        app=request.app,
        paths_filter=lambda key_value: key_value[0].startswith(BASE_API_V6_PREFIX),
        title=f"{request.app.title} v6",
    )
    add_security_to_openapi(openapi_schema)

    return openapi_schema
