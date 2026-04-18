from typing import Any
from uuid import uuid4

import pytest
from faker.proxy import Faker


@pytest.fixture
def page_id():
    return uuid4().hex


@pytest.fixture
def paragraph_id():
    return uuid4().hex


@pytest.fixture
def table_id():
    return uuid4().hex


@pytest.fixture
def key_value_pair_id():
    return uuid4().hex


@pytest.fixture
def update_paragraph_payload(faker: Faker) -> dict[str, Any]:
    return {
        "lines": [
            {"content": faker.text(max_nb_chars=30), "order": 0},
            {"content": faker.text(max_nb_chars=30), "order": 1},
            {"content": faker.text(max_nb_chars=30), "order": 2},
        ],
    }


@pytest.fixture
def update_table_payload(faker: Faker) -> dict[str, Any]:
    return {
        "cells": [
            {
                "content": faker.text(max_nb_chars=30),
                "rowIndex": 0,
                "columnIndex": 0,
            },
            {
                "content": faker.text(max_nb_chars=30),
                "rowIndex": 0,
                "columnIndex": 1,
            },
            {
                "content": faker.text(max_nb_chars=30),
                "rowIndex": 0,
                "columnIndex": 2,
            },
        ],
    }


@pytest.fixture
def update_key_value_pair_payload(faker: "Faker") -> dict[str, Any]:
    return {
        "key": {
            "content": faker.text(max_nb_chars=15),
            "polygon": [
                {"x": faker.pyfloat(min_value=0, max_value=1), "y": faker.pyfloat(min_value=0, max_value=1)}
                for _ in range(4)
            ],
        },
        "value": {
            "content": faker.text(max_nb_chars=15),
            "polygon": [
                {"x": faker.pyfloat(min_value=0, max_value=1), "y": faker.pyfloat(min_value=0, max_value=1)}
                for _ in range(4)
            ],
        },
    }
