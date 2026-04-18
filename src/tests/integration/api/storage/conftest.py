from pathlib import Path

import pytest
from faker.proxy import Faker

from deps_api_gateway.constants import STORAGE_BASE_API_PREFIX, V1_PREFIX
from deps_api_gateway.infrastructure import FormDataBuilder, StorageProxy
from deps_api_gateway.settings import get_storage_settings


@pytest.fixture
def storage_settings():
    return get_storage_settings()


@pytest.fixture
def default_storage(storage_settings):
    return storage_settings.default_storage


@pytest.fixture
def full_storage_url():
    return f"{STORAGE_BASE_API_PREFIX}{V1_PREFIX}/file"


@pytest.fixture
def folder_path(faker: Faker):
    return Path(faker.file_path()).parent


@pytest.fixture
def file_name(faker: Faker):
    return faker.file_name(extension="pdf")


@pytest.fixture
def file_path(folder_path, file_name):
    return f"{folder_path}/{file_name}"


@pytest.fixture
def request_data(faker: Faker, default_storage, file_name):
    return (
        FormDataBuilder()
        .with_file(field_name=StorageProxy.FILE_FIELD_NAME, filename=file_name, content=b"file content")
        .with_field(key="storage", value=default_storage)
        .with_field(key="replaceIfExists", value=str(faker.pybool()))
        .build()
    )


@pytest.fixture
def request_data_without_required(file_name):
    return (
        FormDataBuilder()
        .with_file(field_name=StorageProxy.FILE_FIELD_NAME, filename=file_name, content=b"file content")
        .build()
    )
