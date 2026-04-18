from typing import Any, Callable, Optional

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

__all__ = ["build_openapi_schema"]


def build_openapi_schema(
    app: FastAPI,
    paths_filter: Callable[[tuple[str, Any]], bool],
    title: Optional[str] = None,
    version: Optional[str] = None,
    description: Optional[str] = None,
) -> dict[str, Any]:
    openapi_schema = get_openapi(
        title=app.title if title is None else title,
        version=app.version if version is None else version,
        routes=app.routes,
        description=app.description if description is None else description,
    )
    openapi_schema["paths"] = dict(filter(paths_filter, openapi_schema["paths"].items()))

    return openapi_schema
