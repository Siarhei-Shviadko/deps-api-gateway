from typing import Union, cast

__all__ = ["DocumentResponseValidator"]

from .is_exception import is_exception
from .raise_all import raise_all
from .typehints import CorleoneResponse, DocumentTypeResponse, GenericRestResponse


class DocumentResponseValidator:
    def __init__(self) -> None:
        exception_placeholder = KeyError("Attribute is not filled")
        self._document_task_result: Union[GenericRestResponse, BaseException] = exception_placeholder
        self._corleone_task_result: Union[CorleoneResponse, BaseException] = exception_placeholder
        self._document_type_task_result: Union[list[DocumentTypeResponse], BaseException] = exception_placeholder
        self._ocr_engines_task_result: Union[GenericRestResponse, BaseException] = exception_placeholder
        self._ocr_languages_task_result: Union[GenericRestResponse, BaseException] = exception_placeholder
        self._document_state_result: Union[BaseException, GenericRestResponse] = exception_placeholder

    def for_document(
        self, document_task_result: Union[GenericRestResponse, BaseException]
    ) -> "DocumentResponseValidator":
        self._document_task_result = document_task_result
        return self

    def with_corleone_types(
        self, corleone_task_result: Union[CorleoneResponse, BaseException]
    ) -> "DocumentResponseValidator":
        self._corleone_task_result = corleone_task_result
        return self

    def with_document_type_types(
        self, document_type_result: Union[list[DocumentTypeResponse], BaseException]
    ) -> "DocumentResponseValidator":
        self._document_type_task_result = document_type_result
        return self

    def with_engines(self, engines: Union[GenericRestResponse, BaseException]) -> "DocumentResponseValidator":
        self._ocr_engines_task_result = engines
        return self

    def with_languages(self, languages: Union[GenericRestResponse, BaseException]) -> "DocumentResponseValidator":
        self._ocr_languages_task_result = languages
        return self

    def with_states(self, states: Union[BaseException, GenericRestResponse]) -> "DocumentResponseValidator":
        self._document_state_result = states
        return self

    def validate(self) -> None:
        self._validate()

    def _validate(self):
        to_raise = []
        to_raise.extend(self._validate_doc_types_obtained())
        to_raise.extend(self._validate_other_components_obtained())
        if to_raise:
            raise_all(*to_raise)

    def _validate_other_components_obtained(self):
        return list(
            filter(
                is_exception,
                (
                    self._document_task_result,
                    self._document_state_result,
                    self._ocr_engines_task_result,
                    self._ocr_languages_task_result,
                ),
            )
        )

    def _validate_doc_types_obtained(self) -> list[BaseException]:
        type_exceptions = list(filter(is_exception, (self._document_type_task_result, self._corleone_task_result)))
        if len(type_exceptions) > 1:
            return cast(list[BaseException], type_exceptions)
        return []
