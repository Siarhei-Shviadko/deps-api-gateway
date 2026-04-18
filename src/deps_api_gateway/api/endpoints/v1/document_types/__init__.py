from .document_types import *
from .legacy_document_types import *

__all__ = legacy_document_types.__all__ + document_types.__all__
