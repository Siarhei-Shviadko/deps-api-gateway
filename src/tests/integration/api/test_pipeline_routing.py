import json
from http import HTTPStatus

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    CORLEONE_BASE_API_PREFIX,
    DOCUMENT_BASE_API_PREFIX,
    DOCUMENT_TYPE_BASE_API_PREFIX,
    PLUGIN_EXTRACTION_TYPE,
    V1_PREFIX,
    V2_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
)
from tests.data.json_data import (
    DOCUMENT_DETAIL_RESPONSE_1_JSON,
    DOCUMENT_DETAIL_RESPONSE_2_JSON,
    TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON,
    TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON,
    document_for_old_pipeline,
    document_for_workflow_pipeline,
)

HEADERS = {"deps-token": '{"organisation": "deps-users"}', "content-type": "application/json"}


class TestPipelineRouting:
    document_detail_url_1 = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/{document_for_old_pipeline['_id']}"
    document_detail_url_2 = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/{document_for_workflow_pipeline['_id']}"
    corleone_url = CORLEONE_BASE_API_PREFIX + V1_PREFIX + "/types/{}"
    document_type_url = DOCUMENT_TYPE_BASE_API_PREFIX + V1_PREFIX + "/types/{}"
    document_run_pipeline_url = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/run-pipeline"
    workflow_run_pipeline_url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}" + "/run-{}-pipeline"
    document_run_pipeline_from_step_url = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/run-pipeline-from-step"
    workflow_run_pipeline_from_step_url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V2_PREFIX}/run-pipeline-from-step"
    document_retry_last_step_url = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/retry-last-step"
    workflow_retry_last_step_url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/retry-" + "{}-pipeline-last-step"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "pipeline_data,type_codes,extraction_type",
        [
            (
                {
                    "documentIds": [document_for_old_pipeline["_id"]],
                    "engine": "TESSERACT",
                    "extractData": True,
                    "language": "eng",
                },
                [document_for_old_pipeline["documentType"]],
                None,
            ),
            (
                {
                    "documentIds": [document_for_workflow_pipeline["_id"]],
                    "engine": "TESSERACT",
                    "extractData": True,
                    "language": "eng",
                },
                [document_for_workflow_pipeline["documentType"]],
                "plugin",
            ),
            (
                {
                    "documentIds": [document_for_workflow_pipeline["_id"]],
                    "engine": "TESSERACT",
                    "extractData": True,
                    "language": "eng",
                },
                [document_for_workflow_pipeline["documentType"]],
                "template",
            ),
            (
                {
                    "documentIds": [document_for_old_pipeline["_id"], document_for_workflow_pipeline["_id"]],
                    "engine": "TESSERACT",
                    "extractData": True,
                    "language": "eng",
                },
                [document_for_old_pipeline["documentType"], document_for_workflow_pipeline["documentType"]],
                "template",
            ),
            (
                {
                    "documentIds": [document_for_old_pipeline["_id"], document_for_workflow_pipeline["_id"]],
                    "engine": "TESSERACT",
                    "extractData": True,
                    "language": "eng",
                },
                [document_for_old_pipeline["documentType"], document_for_workflow_pipeline["documentType"]],
                "plugin",
            ),
        ],
    )
    async def test_routing__run_pipeline__successful(
        self,
        client,
        pipeline_data,
        type_codes,
        extraction_type,
        document_type_extraction_type_cache,
    ):
        for type_code in type_codes:
            document_type_extraction_type_cache[type_code] = extraction_type
        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)
            mocked.post(
                self.workflow_run_pipeline_url.format(extraction_type or PLUGIN_EXTRACTION_TYPE),
                status=202,
                body=b"",
            )
            mocked.post(self.document_run_pipeline_url, status=201, body=b"")

            res = await client.post(self.document_run_pipeline_url, headers=HEADERS, data=json.dumps(pipeline_data))

            assert res.status_code == HTTPStatus.ACCEPTED

    @pytest.mark.asyncio
    @pytest.mark.parametrize("extraction_type", ["plugin", "template", None])
    async def test_routing__run_pipeline__workflow_service_raise_error__return_success(
        self,
        client,
        extraction_type,
        document_type_extraction_type_cache,
    ):
        for type_code in [document_for_old_pipeline["documentType"], document_for_workflow_pipeline["documentType"]]:
            document_type_extraction_type_cache[type_code] = extraction_type

        pipeline_data = {
            "documentIds": [document_for_old_pipeline["_id"], document_for_workflow_pipeline["_id"]],
            "engine": "TESSERACT",
            "extractData": True,
            "language": "eng",
        }

        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)
            mocked.post(
                self.workflow_run_pipeline_url.format(extraction_type or PLUGIN_EXTRACTION_TYPE),
                exception=ValueError,
            )
            mocked.post(self.document_run_pipeline_url, status=201, body=b"")

            res = await client.post(self.document_run_pipeline_url, headers=HEADERS, data=json.dumps(pipeline_data))

            assert res.status_code == HTTPStatus.ACCEPTED

    @pytest.mark.asyncio
    @pytest.mark.parametrize("extraction_type", ["plugin", "template", None])
    async def test_routing__run_pipeline__document_service_raise_error__return_success(
        self,
        client,
        extraction_type,
        document_type_extraction_type_cache,
    ):
        for type_code in [document_for_old_pipeline["documentType"], document_for_workflow_pipeline["documentType"]]:
            document_type_extraction_type_cache[type_code] = extraction_type

        pipeline_data = {
            "documentIds": [document_for_old_pipeline["_id"], document_for_workflow_pipeline["_id"]],
            "engine": "TESSERACT",
            "extractData": True,
            "language": "eng",
        }

        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)
            mocked.post(
                self.workflow_run_pipeline_url.format(extraction_type or PLUGIN_EXTRACTION_TYPE),
                status=202,
                body=b"",
            )
            mocked.post(self.document_run_pipeline_url, exception=ValueError)

            res = await client.post(self.document_run_pipeline_url, headers=HEADERS, data=json.dumps(pipeline_data))

            assert res.status_code == HTTPStatus.ACCEPTED

    @pytest.mark.asyncio
    @pytest.mark.parametrize("extraction_type", ["plugin", "template", None])
    async def test_routing__run_pipeline__services_raise_error__error(
        self,
        client,
        extraction_type,
        document_type_extraction_type_cache,
    ):
        for type_code in [document_for_old_pipeline["documentType"], document_for_workflow_pipeline["documentType"]]:
            document_type_extraction_type_cache[type_code] = extraction_type

        pipeline_data = {
            "documentIds": [document_for_old_pipeline["_id"], document_for_workflow_pipeline["_id"]],
            "engine": "TESSERACT",
            "extractData": True,
            "language": "eng",
        }

        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)
            mocked.post(
                self.workflow_run_pipeline_url.format(extraction_type or PLUGIN_EXTRACTION_TYPE),
                exception=ValueError,
            )
            mocked.post(self.document_run_pipeline_url, exception=ValueError)

            res = await client.post(self.document_run_pipeline_url, headers=HEADERS, data=json.dumps(pipeline_data))

            assert res.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.asyncio
    async def test_routing__run_pipeline__unexisting_document__error(self, client):
        pipeline_data = {
            "documentIds": [document_for_old_pipeline["_id"]],
            "engine": "TESSERACT",
            "extractData": True,
            "language": "eng",
        }
        with aioresponses() as mocked:
            mocked.get(self.document_detail_url_1, status=404, body=b'{"code": "not found"}')

            res = await client.post(self.document_run_pipeline_url, headers=HEADERS, data=json.dumps(pipeline_data))

            assert res.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "pipeline_data,type_codes,extraction_type",
        [
            (
                {
                    "documentIds": [document_for_old_pipeline["_id"]],
                    "engine": "TESSERACT",
                    "language": "eng",
                    "step": "preprocess",
                },
                [document_for_old_pipeline["documentType"]],
                None,
            ),
            (
                {
                    "documentIds": [document_for_workflow_pipeline["_id"]],
                    "engine": "TESSERACT",
                    "language": "eng",
                    "step": "preprocess",
                },
                [document_for_workflow_pipeline["documentType"]],
                "template",
            ),
            (
                {
                    "documentIds": [document_for_workflow_pipeline["_id"]],
                    "engine": "TESSERACT",
                    "language": "eng",
                    "step": "preprocess",
                },
                [document_for_workflow_pipeline["documentType"]],
                "plugin",
            ),
            (
                {
                    "documentIds": [document_for_old_pipeline["_id"], document_for_workflow_pipeline["_id"]],
                    "engine": "TESSERACT",
                    "language": "eng",
                    "step": "preprocess",
                },
                [document_for_old_pipeline["documentType"], document_for_workflow_pipeline["documentType"]],
                "plugin",
            ),
            (
                {
                    "documentIds": [document_for_old_pipeline["_id"], document_for_workflow_pipeline["_id"]],
                    "engine": "TESSERACT",
                    "language": "eng",
                    "step": "preprocess",
                },
                [document_for_old_pipeline["documentType"], document_for_workflow_pipeline["documentType"]],
                "template",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_routing__run_pipeline_from_step__successful(
        self,
        client,
        pipeline_data,
        extraction_type,
        type_codes,
        document_type_extraction_type_cache,
    ):
        for type_code in type_codes:
            document_type_extraction_type_cache[type_code] = extraction_type

        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)

            mocked.post(
                self.workflow_run_pipeline_from_step_url,
                status=202,
                body=b"",
            )
            mocked.post(self.document_run_pipeline_from_step_url, status=200, body=b"")

            res = await client.post(
                self.document_run_pipeline_from_step_url, headers=HEADERS, data=json.dumps(pipeline_data)
            )

            assert res.status_code == HTTPStatus.ACCEPTED

    @pytest.mark.asyncio
    @pytest.mark.parametrize("extraction_type", ["plugin", "template", None])
    async def test_routing__run_pipeline_from_step___workflow_service_return_error_successful(
        self,
        client,
        extraction_type,
        document_type_extraction_type_cache,
    ):
        for type_code in [document_for_old_pipeline["documentType"], document_for_workflow_pipeline["documentType"]]:
            document_type_extraction_type_cache[type_code] = extraction_type

        pipeline_data = {
            "documentIds": [document_for_old_pipeline["_id"], document_for_workflow_pipeline["_id"]],
            "engine": "TESSERACT",
            "extractData": True,
            "language": "eng",
        }

        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)
            mocked.post(
                self.workflow_run_pipeline_from_step_url,
                status=500,
                body=b"{'message': 'dont want to work'}",
            )
            mocked.post(self.document_run_pipeline_from_step_url, status=200, body=b"")

            res = await client.post(
                self.document_run_pipeline_from_step_url, headers=HEADERS, data=json.dumps(pipeline_data)
            )

            assert res.status_code == HTTPStatus.ACCEPTED

    @pytest.mark.asyncio
    @pytest.mark.parametrize("extraction_type", ["plugin", "template", None])
    async def test_routing__run_pipeline_from_step___document_service_return_error_successful(
        self,
        client,
        extraction_type,
        document_type_extraction_type_cache,
    ):
        for type_code in [document_for_old_pipeline["documentType"], document_for_workflow_pipeline["documentType"]]:
            document_type_extraction_type_cache[type_code] = extraction_type

        pipeline_data = {
            "documentIds": [document_for_old_pipeline["_id"], document_for_workflow_pipeline["_id"]],
            "engine": "TESSERACT",
            "extractData": True,
            "language": "eng",
        }

        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)
            mocked.post(self.document_run_pipeline_from_step_url, status=500, body=b"{'message': 'dont want to work'}")
            mocked.post(
                self.workflow_run_pipeline_from_step_url,
                status=200,
                body=b"",
            )

            res = await client.post(
                self.document_run_pipeline_from_step_url, headers=HEADERS, data=json.dumps(pipeline_data)
            )

            assert res.status_code == HTTPStatus.ACCEPTED

    @pytest.mark.asyncio
    @pytest.mark.parametrize("extraction_type", ["plugin", "template", None])
    async def test_routing__run_pipeline_from_step___services_return_error__error(
        self,
        client,
        extraction_type,
        document_type_extraction_type_cache,
    ):
        for type_code in [document_for_old_pipeline["documentType"], document_for_workflow_pipeline["documentType"]]:
            document_type_extraction_type_cache[type_code] = extraction_type

        pipeline_data = {
            "documentIds": [document_for_old_pipeline["_id"], document_for_workflow_pipeline["_id"]],
            "engine": "TESSERACT",
            "extractData": True,
            "language": "eng",
        }

        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)

            mocked.post(self.document_run_pipeline_from_step_url, status=500, body=b"{'message': 'dont want to work'}")
            mocked.post(
                self.workflow_run_pipeline_from_step_url,
                status=500,
                body=b"{'message': 'dont want to work'}",
            )

            res = await client.post(
                self.document_run_pipeline_from_step_url, headers=HEADERS, data=json.dumps(pipeline_data)
            )

            assert res.status_code == HTTPStatus.BAD_GATEWAY

    @pytest.mark.asyncio
    @pytest.mark.parametrize("extraction_type", ["plugin", "template", None])
    async def test_routing__run_last_step__workfow_service_successful(
        self,
        client,
        extraction_type,
        document_type_extraction_type_cache,
    ):
        document_type_extraction_type_cache[document_for_workflow_pipeline["documentType"]] = extraction_type
        pipeline_data = {
            "documentId": document_for_workflow_pipeline["_id"],
        }
        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)

            mocked.post(
                self.workflow_retry_last_step_url.format(extraction_type or PLUGIN_EXTRACTION_TYPE),
                status=202,
                body=b"",
            )

            res = await client.post(self.document_retry_last_step_url, headers=HEADERS, data=json.dumps(pipeline_data))

            assert res.status_code == HTTPStatus.ACCEPTED

    @pytest.mark.asyncio
    @pytest.mark.parametrize("extraction_type", ["plugin", "template", None])
    async def test_routing__run_last_step__workflow_service_error__error(
        self,
        client,
        extraction_type,
        document_type_extraction_type_cache,
    ):
        document_type_extraction_type_cache[document_for_workflow_pipeline["documentType"]] = extraction_type
        pipeline_data = {
            "documentId": document_for_workflow_pipeline["_id"],
        }
        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)

            mocked.post(
                self.workflow_run_pipeline_from_step_url,
                status=500,
                body=b"{'message': 'christmas party'}",
            )

            res = await client.post(self.document_retry_last_step_url, headers=HEADERS, data=json.dumps(pipeline_data))

            assert res.status_code == HTTPStatus.BAD_GATEWAY

    @pytest.mark.asyncio
    async def test_routing__run_last_step__document_service_successful(self, client):
        pipeline_data = {
            "documentId": document_for_old_pipeline["_id"],
        }
        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)

            mocked.post(self.document_retry_last_step_url, status=202, body=b"")

            res = await client.post(self.document_retry_last_step_url, headers=HEADERS, data=json.dumps(pipeline_data))

            assert res.status_code == HTTPStatus.ACCEPTED

    @pytest.mark.asyncio
    async def test_routing__run_last_step__document_service_error__error(self, client):
        pipeline_data = {
            "documentId": document_for_old_pipeline["_id"],
        }
        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)

            mocked.post(self.document_retry_last_step_url, status=500, body=b"{'message': 'cristhmas party'}")

            res = await client.post(self.document_retry_last_step_url, headers=HEADERS, data=json.dumps(pipeline_data))

            assert res.status_code == HTTPStatus.BAD_GATEWAY

    @pytest.mark.asyncio
    async def test_routing__pipelines__no_document_ids__error(self, client):
        pipeline_data = {
            "documentIds": [],
            "engine": "TESSERACT",
            "extractData": True,
            "language": "eng",
        }

        with aioresponses() as mocked:
            self._document_detail_mock(mocked)
            self._document_types_mock(mocked)

            res_1 = await client.post(
                self.document_run_pipeline_from_step_url, headers=HEADERS, data=json.dumps(pipeline_data)
            )
            res_2 = await client.post(self.document_run_pipeline_url, headers=HEADERS, data=json.dumps(pipeline_data))

            assert res_1.status_code == HTTPStatus.BAD_REQUEST
            assert res_2.status_code == HTTPStatus.BAD_REQUEST

    def _document_detail_mock(self, mocked):
        mocked.get(self.document_detail_url_1, status=200, body=DOCUMENT_DETAIL_RESPONSE_1_JSON)
        mocked.get(self.document_detail_url_2, status=200, body=DOCUMENT_DETAIL_RESPONSE_2_JSON)

    def _document_types_mock(self, mocked):
        corleone_type_code = TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON["code"]
        document_type_type_code = TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["id"]
        mocked.get(
            self.corleone_url.format(corleone_type_code),
            status=200,
            body=json.dumps(TYPE_RESPONSE_FROM_CORLEONE_SERVICE_JSON),
        )
        mocked.get(
            self.document_type_url.format(document_type_type_code),
            status=200,
            body=json.dumps(TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON),
        )
