import json
from functools import cached_property
from typing import Optional

__all__ = ["DocumentResponseAggregator"]

from .is_exception import is_exception
from .typehints import (
    AggregatedDocument,
    AggregatedDocumentList,
    CodeName,
    CorleoneResponse,
    Document,
    DocumentListProxyResponse,
    DocumentTypeResponse,
    GenericRestResponse,
    ResponseLabel,
    States,
    Status,
)


class DocumentResponseAggregator:
    def __init__(
        self,
    ) -> None:
        self.documents: Optional[DocumentListProxyResponse] = None
        self.corleone_types: Optional[CorleoneResponse] = None
        self.document_type_types: Optional[list[DocumentTypeResponse]] = None
        self.ocr_engines: Optional[list[CodeName]] = None
        self.ocr_languages: Optional[list[CodeName]] = None
        self.document_states: Optional[States] = None

    def for_document(self, document_task_result: GenericRestResponse) -> "DocumentResponseAggregator":
        self.documents = json.loads(document_task_result["content"])
        return self

    def with_corleone_types(self, corleone_task_result: CorleoneResponse) -> "DocumentResponseAggregator":
        self.corleone_types = corleone_task_result
        return self

    def with_document_type_types(
        self, document_type_task_result: list[DocumentTypeResponse]
    ) -> "DocumentResponseAggregator":
        self.document_type_types = document_type_task_result
        return self

    def with_engines(self, ocr_engines_task_result: list[CodeName]) -> "DocumentResponseAggregator":
        self.ocr_engines = ocr_engines_task_result
        return self

    def with_languages(self, ocr_languages_task_result: list[CodeName]) -> "DocumentResponseAggregator":
        self.ocr_languages = ocr_languages_task_result
        return self

    def with_states(self, document_states_task_result: States) -> "DocumentResponseAggregator":
        self.document_states = document_states_task_result
        return self

    def aggregate(self) -> AggregatedDocumentList:
        response_docs: list[AggregatedDocument] = [
            self._aggregate_document(document) for document in self.documents["result"]
        ]
        size, total = self._build_response_meta()
        return {"size": size, "total": total, "result": response_docs}

    @cached_property
    def _document_type_code_name(self) -> dict[str, str]:
        dt_codename: dict[str, str] = {}
        if not is_exception(self.document_type_types):
            dt_codename.update({dt["id"]: dt["documentType"] for dt in self.document_type_types})
        if not is_exception(self.corleone_types):
            dt_codename.update({dt["code"]: dt["name"] for dt in self.corleone_types["result"]})
        return dt_codename

    @cached_property
    def _language_code_name(self) -> dict[str, str]:
        return {lan["code"]: lan["name"] for lan in self.ocr_languages}

    @cached_property
    def _engine_code_name(self) -> dict[str, str]:
        return {eng["code"]: eng["name"] for eng in self.ocr_engines}

    def _build_response_meta(self):
        size = self.documents["meta"]["size"]
        total = self.documents["meta"]["total"]
        return size, total

    def _aggregate_document(self, document: Document) -> AggregatedDocument:
        doctype_code, lang_code, eng_code, doc_state = (
            document["documentType"],
            document["language"],
            document["engine"],
            document["state"],
        )
        doctype_name = self._document_type_code_name.get(doctype_code)
        document_type_dict: Optional[CodeName] = self._build_codename(doctype_code, doctype_name)
        language_dict: Optional[CodeName] = self._build_codename(lang_code, self._language_code_name.get(lang_code))
        engine_dict: Optional[CodeName] = self._build_codename(eng_code, self._engine_code_name.get(eng_code))
        state_dict = self._build_states(doc_state)
        labels: list[ResponseLabel] = self._build_labels(document)
        return {
            "id": document["_id"],
            "title": document["title"],
            "date": document["date"],
            "documentType": document_type_dict,
            "language": language_dict,
            "engine": engine_dict,
            "state": state_dict,
            "labels": labels,
            "reviewer": document["reviewer"],
        }

    def _build_states(self, doc_state) -> Optional[CodeName]:
        state: Optional[Status] = self.document_states.get(doc_state)
        if not state:
            return None
        state_title = state["title"]
        return self._build_codename(doc_state, state_title)

    @staticmethod
    def _build_labels(document) -> list[ResponseLabel]:
        document_labels = document.get("labels", [])
        return [{"id": label["_id"], "name": label["name"]} for label in document_labels]

    @staticmethod
    def _build_codename(code: Optional[str], name: Optional[str]) -> Optional[CodeName]:
        return None if None in {code, name} else {"code": code, "name": name}
