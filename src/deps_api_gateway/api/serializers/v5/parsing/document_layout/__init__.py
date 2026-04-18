from .document_layout import *
from .merged_table import *
from .page import *
from .point import *
from .update_image import *
from .update_paragraph_request import *
from .update_table_request import *

__all__ = (
    page.__all__
    + document_layout.__all__
    + point.__all__
    + merged_table.__all__
    + update_image.__all__
    + update_paragraph_request.__all__
    + update_table_request.__all__
)
