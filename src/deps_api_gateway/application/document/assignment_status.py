from enum import Enum

__all__ = ["DocumentAssignmentStatus"]


class DocumentAssignmentStatus(str, Enum):
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    HOLD = "hold"
