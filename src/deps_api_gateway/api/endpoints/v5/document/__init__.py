from fastapi import APIRouter

from .analysis import analysis_router
from .comments import comments_router
from .conversation import conversation_router
from .document import documents_router
from .document_type import document_type_router
from .extract_data import extract_data_router
from .extracted_data import extracted_data_router
from .files import files_router
from .labels import labels_router
from .llm_coordinates import llm_coordinates_router
from .outputs import outputs_router
from .parsing import parsing_router
from .semantic_layout import semantic_layout_router
from .states import states_router
from .supplement import supplement_router
from .unified_data import unified_data_router
from .validation import validation_router

__all__ = ["document_router"]

document_router = APIRouter()
document_router.include_router(validation_router)
document_router.include_router(comments_router)
document_router.include_router(labels_router)
document_router.include_router(states_router)
document_router.include_router(unified_data_router)
document_router.include_router(outputs_router)
document_router.include_router(conversation_router)
document_router.include_router(extracted_data_router)
document_router.include_router(semantic_layout_router)
document_router.include_router(files_router)
document_router.include_router(supplement_router)
document_router.include_router(parsing_router)
document_router.include_router(document_type_router)
document_router.include_router(analysis_router)
document_router.include_router(extract_data_router)
document_router.include_router(llm_coordinates_router)
document_router.include_router(documents_router)  # Should be included the last
