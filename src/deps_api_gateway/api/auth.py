import json
from http import HTTPStatus
from typing import Any

from fastapi import Request

from deps_api_gateway.domain.exceptions import AuthError, AuthorizationError
from deps_api_gateway.infrastructure import user

__all__ = ["get_deps_token", "set_user_from_token"]

PUBLIC_ENDPOINTS_POSTFIXES = (
    "/debug/500",
    "/healthcheck",
    "/service-info/version",
    "/docs",
    "/openapi.json",
    "/favicon.ico",
    # Validation swagger static resources
    "/swagger-ui.css",
    "/lib/jquery.min.js",
    "/swagger-ui-bundle.js",
    "/swagger-ui-standalone-preset.js",
    "/favicon-32x32.png",
)


def get_deps_token(request: Request) -> str:
    if deps_token := request.headers.get("deps-token"):
        return deps_token

    raise AuthorizationError("Deps token is not provided")


def set_user_from_token(request: Request) -> None:
    if request.url.path.endswith(PUBLIC_ENDPOINTS_POSTFIXES):
        return

    try:
        deps_token = json.loads(request.headers["deps-token"])
        _validate_deps_token(deps_token)
        deps_token["deps_token"] = request.headers["deps-token"]
        user.set(deps_token)

    except KeyError:
        raise AuthError("Deps-token doesn't provided.")

    except TypeError:
        raise AuthError("Provided deps-token isn't correct.")


def _validate_deps_token(deps_token: dict[str, Any]) -> None:
    if not deps_token:
        raise AuthError("Deps-token validation fails. Deps-token is invalid.")
    elif not deps_token.get("organisation"):
        raise AuthError(
            detail="User without organisation.",
            status_code=HTTPStatus.FORBIDDEN,
        )
