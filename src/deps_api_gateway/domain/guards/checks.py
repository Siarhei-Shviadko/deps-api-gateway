import re
from typing import Any, Protocol, Type, TypeVar

from deps_api_gateway.domain.exceptions import IllegalArgument
from deps_api_gateway.domain.guards.attribute_name import AttributeName

T = TypeVar("T", contravariant=True)


class Check(Protocol[T]):
    def is_correct(self, domain_obj: Any, value: T, attribute_name: AttributeName) -> None:
        ...  # noqa: WPS428


class NoneCheck:
    def is_correct(self, domain_obj: Any, value: T, attribute_name: AttributeName) -> None:
        if value is None:
            raise IllegalArgument(
                f"Attribute {attribute_name.public} for {domain_obj.__class__.__name__} object should be provided."
            )


class TypeCheck:
    def __init__(self, type_: Type[T]) -> None:
        self._type = type_

    def is_correct(self, domain_obj: Any, value: T, attribute_name: AttributeName) -> None:
        if not isinstance(value, self._type):
            raise IllegalArgument(
                f"Attribute {attribute_name.public} for {domain_obj.__class__.__name__} object should be {self._type.__name__}."
            )


class ImmutableCheck:
    def is_correct(self, domain_obj: Any, value: T, attribute_name: AttributeName) -> None:
        if hasattr(domain_obj, attribute_name.private) and getattr(domain_obj, attribute_name.private) is not None:
            raise IllegalArgument(
                f"Attribute {attribute_name.public} for {domain_obj.__class__.__name__} object cannot be changed."
            )


class FormatCheck:
    def __init__(self, pattern: str) -> None:
        self._pattern = pattern

    def is_correct(self, domain_obj: Any, value: str, attribute_name: AttributeName) -> None:
        if not re.fullmatch(self._pattern, value):
            raise IllegalArgument(
                (
                    "Attribute {0} for {1} object should not contain special symbols.".format(
                        attribute_name.public, domain_obj.__class__.__name__
                    )
                )
            )
