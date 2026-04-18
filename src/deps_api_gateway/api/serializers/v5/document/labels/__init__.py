from .add_label_on_document_request import *
from .create_label_request import *
from .get_labels_response import *
from .label import *

__all__ = (
    label.__all__ + get_labels_response.__all__ + create_label_request.__all__ + add_label_on_document_request.__all__
)
