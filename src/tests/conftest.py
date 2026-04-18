import asyncio
import json
import uuid
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from faker import Faker
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from multidict import CIMultiDict, CIMultiDictProxy

from deps_api_gateway import api
from deps_api_gateway.application import ProxyResponse
from deps_api_gateway.entrypoint import create_fastapi

fake = Faker()


@pytest_asyncio.fixture(scope="session")
async def app() -> AsyncGenerator:
    fastapi_app = create_fastapi()
    async with LifespanManager(fastapi_app):
        yield fastapi_app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        yield client


@pytest.fixture(scope="session")
def containers(app):
    yield app.containers


@pytest.fixture()
def application(containers):
    return containers.application


@pytest.fixture
def routers(containers):
    return containers.routers


@pytest.fixture
def domain_services(containers):
    return containers.domain_services


@pytest.fixture
def document_type_source_cache(domain_services):
    yield domain_services.document_type_source_cache()
    domain_services.document_type_source_cache().clear()


@pytest.fixture
def document_type_code_cache(domain_services):
    yield domain_services.document_type_code_cache()
    domain_services.document_type_code_cache().clear()


@pytest.fixture
def document_type_extraction_type_cache(domain_services):
    yield domain_services.document_type_extraction_type_cache()
    domain_services.document_type_extraction_type_cache().clear()


@pytest.fixture
def rare_caches(domain_services):
    yield domain_services.rarely_updatable_cache()
    domain_services.rarely_updatable_cache().clear()


@pytest.fixture
def prototype_id():
    return uuid.uuid4().hex


@pytest.fixture
def template_id():
    return uuid.uuid4().hex


@pytest.fixture
def template_version_id():
    return uuid.uuid4().hex


@pytest.fixture
def layout_id():
    return uuid.uuid4().hex


@pytest.fixture
def document_layout_id():
    return uuid.uuid4().hex


@pytest.fixture
def tenant_id():
    return uuid.uuid4().hex


@pytest.fixture
def organisation_id() -> str:
    return uuid.uuid4().hex


@pytest.fixture
def user_id() -> str:
    return uuid.uuid4().hex


@pytest.fixture(autouse=True)
def mocked_middleware(monkeypatch, mocker):
    monkeypatch.setattr(api.auth, "set_user_from_token", mocker.Mock({}))


@pytest.fixture
def document_type_id():
    return uuid.uuid4().hex


@pytest.fixture
def extractor_id():
    return uuid.uuid4().hex


@pytest.fixture
def document_id():
    return uuid.uuid4().hex


@pytest.fixture
def file_id():
    return uuid.uuid4().hex


@pytest.fixture
def label_id():
    return uuid.uuid4().hex


@pytest.fixture
def field_code():
    return uuid.uuid4().hex


@pytest.fixture
def external_validator_name():
    return uuid.uuid4().hex


@pytest.fixture
def external_validator_url():
    return fake.url()


@pytest.fixture
def completion_code():
    return uuid.uuid4().hex


@pytest.fixture
def validator_code():
    return uuid.uuid4().hex


@pytest.fixture
def validation_rule_name():
    return uuid.uuid4().hex


@pytest.fixture
def group_id() -> str:
    return uuid.uuid4().hex


@pytest.fixture
def gen_ai_classifier_id() -> str:
    return uuid.uuid4().hex


@pytest.fixture
def ok_proxy_response__maker():
    def _make_ok_proxy_response(data: dict):
        return ProxyResponse(
            status_code=200,
            headers=CIMultiDictProxy(CIMultiDict()),
            content=json.dumps(data),  # type: ignore
        )

    return _make_ok_proxy_response


@pytest.fixture
def not_ok_proxy_response__maker():
    def _make_not_ok_proxy_response(status_code: int, data: dict):
        return ProxyResponse(
            status_code=status_code,
            headers=CIMultiDictProxy(CIMultiDict()),
            content=json.dumps(data),  # type: ignore
        )

    return _make_not_ok_proxy_response


@pytest.fixture
def profile_id():
    return uuid.uuid4().hex


@pytest.fixture
def output_id():
    return uuid.uuid4().hex
