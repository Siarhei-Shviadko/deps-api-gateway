from enum import Enum

__all__ = ["UserSortingField"]


class UserSortingField(str, Enum):
    FULL_NAME_ASC = "firstName_lastName.asc"
    FULL_NAME_DESC = "firstName_lastName.desc"
