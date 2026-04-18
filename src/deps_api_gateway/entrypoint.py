import logging
import os
from typing import Awaitable, Callable

import uvicorn
from async_rest_client import Methods
from fastapi import FastAPI, Request
from fastapi.responses import Response

from deps_api_gateway import api, constants, csrf
from deps_api_gateway.api.endpoints.docs import docs_router
from deps_api_gateway.api.endpoints.service_info import service_info_router
from deps_api_gateway.api.error_handlers import (
    json_api_gateway_exception_error_handler,
    register_error_handler,
)
from deps_api_gateway.containers import Containers
from deps_api_gateway.domain.exceptions import AuthError
from deps_api_gateway.domain.exceptions.csrf import CsrfValidationError
from deps_api_gateway.middleware.authorization import AuthorizationMiddleware
from deps_api_gateway.settings import Settings

logger = logging.getLogger(__name__)


def init_containers(settings: Settings) -> Containers:
    containers = Containers()
    containers.config.from_dict(settings.model_dump())
    containers.init_resources()

    containers.wire(packages=(api,))
    containers.application.wire(packages=(api,))

    return containers


def create_fastapi() -> FastAPI:
    settings = Settings()
    containers: Containers = init_containers(settings)
    _base_service_init(containers)

    fastapi_app = FastAPI(
        title=constants.PROJECT_NAME,
        version=containers.config.version(),
        description=constants.DESCRIPTION,
        openapi_url=None,  # We add separate docs pages for different api version
    )

    fastapi_app.containers = containers

    add_routers(fastapi_app)

    register_auth(fastapi_app)

    register_error_handler(fastapi_app)

    register_csrf(fastapi_app, containers)

    if containers.config.authorization_enabled():
        fastapi_app.add_middleware(AuthorizationMiddleware, iam_url=containers.config.iam_url())

    if containers.config.instrumentation_enabled():
        from deps_observability_instrumentation import (  # noqa: WPS433
            instrument_fast_api,
        )

        instrument_fast_api(fastapi_app)

    return fastapi_app


def register_csrf(app: FastAPI, container: Containers) -> None:
    csrf_config = container.config.csrf()
    if not csrf_config["enabled"]:
        return

    csrf_methods = csrf_config["methods"]

    @app.middleware("http")
    async def csrf_middleware(  # noqa: WPS430
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if request.method in csrf_methods:
            try:
                await csrf.validate_csrf_token(request)
            except CsrfValidationError as err:
                return json_api_gateway_exception_error_handler(err, err.status_code)
        return await call_next(request)


def register_auth(app: FastAPI):
    @app.middleware("http")
    async def handle_authorization(  # noqa: WPS430
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        try:
            api.auth.set_user_from_token(request)
        except AuthError as err:
            return json_api_gateway_exception_error_handler(err, err.status_code)
        return await call_next(request)


def add_routers(fastapi_app: FastAPI):
    api_methods = list(Methods)

    fastapi_app.include_router(service_info_router, prefix=constants.API_PREFIX)
    fastapi_app.include_router(api.router)

    fastapi_app.add_route(
        path=f"{constants.CORLEONE_BASE_API_PREFIX}/{{path:path}}",
        route=fastapi_app.containers.routers.corleone_router().route,
        methods=api_methods,
    )
    fastapi_app.add_route(
        path=f"{constants.PREPROCESS_BASE_API_PREFIX}/{{path:path}}",
        route=fastapi_app.containers.routers.preprocess_router().route,
        methods=api_methods,
    )

    fastapi_app.add_route(
        path=f"{constants.VALIDATION_BASE_PREFIX}/{{path:path}}",
        route=fastapi_app.containers.routers.validation_router().route,
        methods=api_methods,
    )
    fastapi_app.add_route(
        path=f"{constants.PROTOTYPE_BASE_API_PREFIX}/{{path:path}}",
        route=fastapi_app.containers.routers.prototype_router().route,
        methods=api_methods,
    )
    fastapi_app.add_route(
        path=f"{constants.TEMPLATE_BASE_API_PREFIX}/{{path:path}}",
        route=fastapi_app.containers.routers.template_router().route,
        methods=api_methods,
    )
    fastapi_app.add_route(
        path=f"{constants.DOCUMENT_TYPE_BASE_API_PREFIX}/{{path:path}}",
        route=fastapi_app.containers.routers.document_type_router().route,
        methods=api_methods,
    )

    # Router to the document service must be last in the list of routes.
    fastapi_app.add_route(
        path=f"{constants.DOCUMENT_BASE_API_PREFIX}/{{path:path}}",
        route=fastapi_app.containers.routers.document_router().route,
        methods=api_methods,
    )

    if fastapi_app.containers.config.documentation_enabled():
        fastapi_app.include_router(docs_router)


def run_api():
    use_web_concurrency = "WEB_CONCURRENCY" in os.environ
    env = os.getenv("ENV", "prod")
    options = {
        "host": "0.0.0.0",  # noqa: S104
        "port": 8000,
        "log_level": os.getenv("LOG_LEVEL", "debug").lower(),
        "workers": int(os.getenv("WEB_CONCURRENCY")) if use_web_concurrency else 3,
        "reload": env == "development",
        "debug": env == "development",
    }

    uvicorn.run("deps_api_gateway.entrypoint:create_fastapi", **options)


def _base_service_init(containers: Containers) -> None:
    if containers.config.instrumentation_enabled():
        logger.info("Instrumentation enabled.")
        from deps_observability_instrumentation import (  # noqa: WPS433
            setup_instrumentation,
        )

        setup_instrumentation()
