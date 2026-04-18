from enum import Enum

__all__ = ["InvitationSortingField"]


class InvitationSortingField(str, Enum):
    EMAIL_DESC = "email.desc"
    EMAIL_ASC = "email.asc"
