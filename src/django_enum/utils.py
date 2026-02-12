"""Utility routines for django_enum."""

import sys
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum, Flag, IntFlag
from importlib.util import find_spec
from typing import (
    TYPE_CHECKING,
    Any,
    Generator,
    TypeVar,
    get_args,
)

__all__ = [
    "choices",
    "names",
    "labels",
    "values",
    "determine_primitive",
    "with_typehint",
    "SupportedPrimitive",
    "decimal_params",
    "get_set_values",
    "get_set_bits",
    "decompose",
    "members",
]


PROPERTIES_ENABLED = find_spec("enum_properties")
"""
True if enum-properties is installed, False otherwise.
"""

T = TypeVar("T")
E = TypeVar("E", bound=Enum)
F = TypeVar("F", bound=Flag)

SupportedPrimitive = int | str | float | date | datetime | time | timedelta | Decimal


def with_typehint(baseclass: type[T]) -> type[T]:
    """
    Change inheritance to add Field type hints when type checking is running.
    This is just more simple than defining a Protocol - revisit if Django
    provides Field protocol - should also just be a way to create a Protocol
    from a class?

    This is icky but it works - revisit in future.
    """
    if TYPE_CHECKING:
        return baseclass  # pragma: no cover
    return object  # type: ignore


def choices(
    enum_cls: type[Enum] | None, override: bool = False, aliases: bool = True
) -> list[tuple[Any, str]]:
    """
    Get the Django choices for an enumeration type. If the enum type has a
    choices attribute, it will be used. Otherwise, the choices will be derived
    from value, label pairs if the enumeration type has a label attribute, or
    the name attribute if it does not.

    This is used for compat with enums that do not inherit from Django's
    Choices type.

    :param enum_cls: The enumeration type
    :param override: Do not defer to choices attribute on the class if True
    :param aliases: Include first-class aliases in the result if True (default: True)
    :return: A list of (value, label) pairs
    """
    return (
        (getattr(enum_cls, "choices", []) if not override else [])
        or (
            [
                *(
                    [(None, getattr(enum_cls, "__empty__"))]
                    if hasattr(enum_cls, "__empty__")
                    else []
                ),
                *[
                    (member.value, getattr(member, "label", getattr(member, "name")))
                    for member in members(enum_cls, aliases=aliases)
                ],
            ]
        )
        if enum_cls
        else []
    )


def names(
    enum_cls: type[Enum] | None, override: bool = False, aliases: bool = True
) -> list[Any]:
    """
    Return a list of names to use for the enumeration type. This is used
    for compat with enums that do not inherit from Django's Choices type.

    :param enum_cls: The enumeration type
    :param override: Do not defer to names attribute on the class if True
    :param aliases: Include first-class aliases in the result if True (default: True)
    :return: A list of labels
    """
    return (
        (getattr(enum_cls, "names", []) if not override else [])
        or (
            [
                *(["__empty__"] if hasattr(enum_cls, "__empty__") else []),
                *[member.name for member in members(enum_cls, aliases=aliases)],
            ]
        )
        if enum_cls
        else []
    )


def labels(enum_cls: type[Enum] | None) -> list[Any]:
    """
    Return a list of labels to use for the enumeration type. See choices.

    This is used for compat with enums that do not inherit from Django's
    Choices type.

    :param enum_cls: The enumeration type
    :return: A list of labels
    """
    return getattr(enum_cls, "labels", [label for _, label in choices(enum_cls)])


def values(enum_cls: type[Enum] | None) -> list[Any]:
    """
    Return a list of the values of an enumeration type.

    This is used for compat with enums that do not inherit from Django's
    Choices type.

    :param enum_cls: The enumeration type
    :return: A list of values
    """
    return getattr(enum_cls, "values", [value for value, _ in choices(enum_cls)])


def determine_primitive(enum: type[Enum]) -> type | None:
    """
    Determine the python type most appropriate to represent all values of the
    enumeration class. The primitive type determination algorithm is thus:

        * Determine the types of all the values in the enumeration
        * Determine the first supported primitive type in the enumeration class
          inheritance tree
        * If there is only one value type, use its type as the primitive
        * If there are multiple value types and they are all subclasses of
          the class primitive type, use the class primitive type. If there is
          no class primitive type use the first supported primitive type that
          all values are symmetrically coercible to. If there is no such type,
          return None

    By definition all values of the enumeration with the exception of None
    may be coerced to the primitive type and vice-versa.

    :param enum: The enumeration class to determine the primitive type for
    :return: A python type or None if no primitive type could be determined
    """
    primitive = None
    for prim in enum.__mro__:
        if issubclass(prim, get_args(SupportedPrimitive)):
            primitive = prim
            break
    value_types = set()
    for value in values(enum):
        if value is not None:
            value_types.add(type(value))

    if len(value_types) > 1 and primitive is None:
        for candidate in get_args(SupportedPrimitive):
            works = True
            for value in values(enum):
                if value is None:
                    continue
                try:
                    # test symmetric coercibility
                    works &= type(value)(candidate(value)) == value
                except Exception:
                    works = False
            if works:
                return candidate
    elif value_types:
        return list(value_types).pop()
    return primitive


def is_power_of_two(n: int) -> bool:
    """
    Check if an integer is a power of two.

    :param n: The integer to check
    :return: True if the number is a power of two, False otherwise
    """
    return n != 0 and (n & (n - 1)) == 0


def decimal_params(
    enum: type[Enum] | None,
    decimal_places: int | None = None,
    max_digits: int | None = None,
) -> dict[str, int]:
    """
    Determine the maximum number of digits and decimal places required to
    represent all values of the enumeration class.

    :param enum: The enumeration class to determine the decimal parameters for
    :param decimal_places: Use this value for decimal_places rather than
        the computed value
    :param max_digits: Use this value for max_digits rather than the computed
        value
    :return: A tuple of (max_digits, decimal_places)
    """
    decimal_places = decimal_places or max(
        [0]
        + [len(str(value).split(".")[1]) for value in values(enum) if "." in str(value)]
    )
    max_digits = max_digits or (
        decimal_places
        + max(
            [0] + [len(str(value).split(".", maxsplit=1)[0]) for value in values(enum)]
        )
    )
    return {"max_digits": max_digits, "decimal_places": decimal_places}


def get_set_bits(flag: int | IntFlag | None) -> list[int]:
    """
    Return the indices of the bits set in the flag.

    :param flag: The flag to get the set bits for, value must be an int.
    :return: A list of indices of the set bits
    """
    if flag:
        return [i for i in range(flag.bit_length()) if flag & (1 << i)]
    return []


def get_set_values(flag: int | IntFlag | None) -> list[int]:
    """
    Return the integers corresponding to the flags set on the IntFlag or integer.

    :param flag: The flag to get the set bits for, value must be an int.
    :return: A list of flag integers
    """
    if flag:
        return [1 << i for i in range(flag.bit_length()) if (flag >> i) & 1]
    return []


def decompose(flags: F | None) -> list[F]:
    """
    Get the activated flags in a :class:`~enum.Flag` instance. For example:

    .. code-block:: python

        class Permissions(IntFlag):

            READ    = 1 << 0
            WRITE   = 1 << 1
            EXECUTE = 1 << 2

        assert decompose(Permissions.READ | Permissions.WRITE) == (
            [Permissions.READ, Permissions.Write]
        )


    :param: flags: The flag instance to decompose
    :return: A list of the :class:`~enum.Flag` instances comprising the flag.
    """
    if not flags:
        return []
    return [
        flg
        for flg in type(flags).__members__.values()
        if flg in flags and flg is not type(flags)(0)
    ]


def members(enum: type[E], aliases: bool = True) -> Generator[E, None, None]:
    """
    Get the members of an enumeration class. This can be tricky to do
    in a python version agnostic way, so it is recommended to
    use this function.

    .. note:

        Composite flag values, such as `A | B` when named on a
        :class:`~enum.IntFlag` class are considered aliases by this function.

    :param enum_cls: The enumeration class
    :param aliases: Include aliases in the result if True (default: True)
    :return: A generator that yields the enumeration members
    """
    if aliases:
        if PROPERTIES_ENABLED:
            from enum_properties import SymmetricMixin

            if issubclass(enum, SymmetricMixin):
                for member in getattr(enum, "__first_class_members__", []):
                    yield enum[member]  # type: ignore[index]
                return
        yield from enum.__members__.values()
    else:
        if issubclass(enum, Flag) and (
            issubclass(enum, int)
            or isinstance(next(iter(enum.__members__.values())).value, int)
        ):
            for name in enum._member_names_:
                en = enum[name]
                value = en.value
                if value < 0 or is_power_of_two(value):
                    yield en  # type: ignore[misc]
        elif sys.version_info[:2] >= (3, 11):
            yield from enum  # type: ignore[misc]
        else:
            for name in enum._member_names_:
                yield enum[name]  # type: ignore[misc]
