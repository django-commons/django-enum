"""
Type stubs for django_enum.fields.

EnumField uses a metaclass (EnumFieldFactory) at runtime to dynamically choose
the correct Django field base class. Because mypy/pyright cannot track that
metaclass __call__ through generic type parameters we declare the public API
here so that:

  * EnumField[PrimitiveT, EnumT] properly inherits Field[PrimitiveT | EnumT, EnumT]
  * null=True overloads make the get-type Optional (silences the django-stubs plugin
    warning "is nullable but its generic get type parameter is not optional")
  * Concrete subclasses (EnumCharField etc.) do NOT inherit from the matching
    Django concrete field (CharField, IntegerField …) in the stub, which
    prevents the django-stubs _pyi_private_set_type / _pyi_private_get_type
    attributes from overriding EnumField's own generic parameters.

Constructor overloads use __new__ rather than the mypy-only self-annotation
pattern on __init__, so both mypy and pyright correctly resolve the generic
type parameters from the null= and primitive= arguments.
"""

from collections.abc import Sequence
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum, Flag
from typing import Any, Generic, Literal, TypeVar, overload

from django.db.models import (
    BigIntegerField,
    BinaryField,
    Field,
    IntegerField,
    Model,
    PositiveBigIntegerField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    SmallIntegerField,
)
from django.db.models.query_utils import DeferredAttribute

from django_enum.utils import SupportedPrimitive

# Class-level TypeVars (encode the generic parameters of each field class)
PrimitiveT = TypeVar("PrimitiveT", bound=SupportedPrimitive)
EnumT = TypeVar("EnumT", bound=Enum | None)
FlagT = TypeVar("FlagT", bound=Flag | None)

# Method-level TypeVars for __new__ overloads (bound without None so that
# EnumT | None in the return type correctly expresses nullable fields)
_ET = TypeVar("_ET", bound=Enum)
_FT = TypeVar("_FT", bound=Flag)
_PT = TypeVar("_PT", bound=SupportedPrimitive)

MAX_CONSTRAINT_NAME_LENGTH: int

class _DatabaseDefault: ...

class EnumValidatorAdapter:
    wrapped: type
    allow_null: bool
    def __init__(self, wrapped: type, allow_null: bool) -> None: ...
    def __call__(self, value: Any) -> Any: ...
    def __eq__(self, other: object) -> bool: ...
    def __getattribute__(self, name: str) -> Any: ...

class ToPythonDeferredAttribute(DeferredAttribute, Generic[PrimitiveT, EnumT]):
    @overload  # type: ignore[override]
    def __get__(
        self, instance: None, owner: Any
    ) -> ToPythonDeferredAttribute[PrimitiveT, EnumT]: ...
    @overload
    def __get__(self, instance: Model, owner: Any) -> EnumT: ...
    def __set__(self, instance: Model, value: PrimitiveT | EnumT | None) -> None: ...

# ---------------------------------------------------------------------------
# EnumField
# ---------------------------------------------------------------------------
# The class intentionally inherits from Field[PrimitiveT | EnumT, EnumT] here
# in the stub (not in the .py) so that the mypy django-stubs plugin can map
# the two generic parameters directly to Field's _ST / _GT type vars.
#
# Four __new__ overloads cover the {null=False, null=True} x
# {primitive given, primitive omitted} matrix.  When primitive is omitted
# _PT cannot be inferred, so we fall back to Any.
# ---------------------------------------------------------------------------

class EnumField(Field[PrimitiveT | EnumT, EnumT], Generic[PrimitiveT, EnumT]):
    """
    A Django model field that stores an enumeration value.
    """

    descriptor_class: type[ToPythonDeferredAttribute[Any, Any]]

    @property
    def enum(self) -> type[EnumT] | None: ...
    @property
    def strict(self) -> bool: ...
    @property
    def coerce(self) -> bool: ...
    @property
    def constrained(self) -> bool: ...
    @property
    def primitive(self) -> type[PrimitiveT] | None: ...

    # __init__ overrides Field.__init__ so that pyright uses this signature
    # for parameter validation instead of Field.__init__(verbose_name, ...).
    def __init__(
        self,
        enum: type[Enum] | None = ...,
        primitive: type[SupportedPrimitive] | None = ...,
        strict: bool = ...,
        coerce: bool = ...,
        constrained: bool | None = ...,
        null: bool = ...,
        **kwargs: Any,
    ) -> None: ...

    # null=False, primitive not supplied → PrimitiveT=Any
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: None = ...,
        strict: bool = ...,
        coerce: bool = ...,
        constrained: bool | None = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> EnumField[Any, _ET]: ...

    # null=False, primitive supplied → PrimitiveT inferred
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[_PT] = ...,
        strict: bool = ...,
        coerce: bool = ...,
        constrained: bool | None = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> EnumField[_PT, _ET]: ...

    # null=True, primitive not supplied
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: None = ...,
        strict: bool = ...,
        coerce: bool = ...,
        constrained: bool | None = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> EnumField[Any, _ET | None]: ...

    # null=True, primitive supplied
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[_PT] = ...,
        strict: bool = ...,
        coerce: bool = ...,
        constrained: bool | None = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> EnumField[_PT, _ET | None]: ...
    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]: ...
    @staticmethod
    def constraint_name(
        model_class: type[Model], field_name: str, enum: type[EnumT]
    ) -> str: ...

# ---------------------------------------------------------------------------
# Concrete enum fields
# ---------------------------------------------------------------------------
# These do NOT inherit from the matching Django concrete field in the stub.
# Doing so would pull in _pyi_private_set_type / _pyi_private_get_type from
# the django-stubs for those fields, which would override EnumField's
# carefully constructed generic parameters.  The runtime .py files keep the
# proper Django inheritance; here we only need it right for type checking.
# ---------------------------------------------------------------------------

class EnumCharField(EnumField[str, EnumT], Generic[EnumT]):
    """A database field supporting enumerations with character values."""

    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[str] | None = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> EnumCharField[_ET]: ...
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[str] | None = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> EnumCharField[_ET | None]: ...

class EnumFloatField(EnumField[float, EnumT], Generic[EnumT]):
    """A database field supporting enumerations with floating point values."""

    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[float] | None = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> EnumFloatField[_ET]: ...
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[float] | None = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> EnumFloatField[_ET | None]: ...

class IntEnumField(EnumField[int, EnumT], Generic[EnumT]):
    """Base class for integer-backed enum fields."""

    @property
    def bit_length(self) -> int: ...
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[int] | None = ...,
        bit_length: int | None = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> IntEnumField[_ET]: ...
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[int] | None = ...,
        bit_length: int | None = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> IntEnumField[_ET | None]: ...

class EnumSmallIntegerField(IntEnumField[EnumT], SmallIntegerField, Generic[EnumT]):
    """Enum field backed by a SmallIntegerField (2 bytes)."""

class EnumPositiveSmallIntegerField(
    IntEnumField[EnumT], PositiveSmallIntegerField, Generic[EnumT]
):
    """Enum field backed by a PositiveSmallIntegerField (2 bytes)."""

class EnumIntegerField(IntEnumField[EnumT], IntegerField, Generic[EnumT]):
    """Enum field backed by an IntegerField (32 bytes)."""

class EnumPositiveIntegerField(
    IntEnumField[EnumT], PositiveIntegerField, Generic[EnumT]
):
    """Enum field backed by a PositiveIntegerField (32 bytes)."""

class EnumBigIntegerField(IntEnumField[EnumT], BigIntegerField, Generic[EnumT]):
    """Enum field backed by a BigIntegerField (64 bytes)."""

class EnumPositiveBigIntegerField(
    IntEnumField[EnumT], PositiveBigIntegerField, Generic[EnumT]
):
    """Enum field backed by a PositiveBigIntegerField (64 bytes)."""

class EnumDateField(EnumField[date, EnumT], Generic[EnumT]):
    """A database field supporting enumerations with date values."""

    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[date] | None = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> EnumDateField[_ET]: ...
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[date] | None = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> EnumDateField[_ET | None]: ...

class EnumDateTimeField(EnumField[datetime, EnumT], Generic[EnumT]):
    """A database field supporting enumerations with datetime values."""

    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[datetime] | None = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> EnumDateTimeField[_ET]: ...
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[datetime] | None = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> EnumDateTimeField[_ET | None]: ...

class EnumDurationField(EnumField[timedelta, EnumT], Generic[EnumT]):
    """A database field supporting enumerations with duration values."""

    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[timedelta] | None = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> EnumDurationField[_ET]: ...
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[timedelta] | None = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> EnumDurationField[_ET | None]: ...

class EnumTimeField(EnumField[time, EnumT], Generic[EnumT]):
    """A database field supporting enumerations with time values."""

    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[time] | None = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> EnumTimeField[_ET]: ...
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[time] | None = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> EnumTimeField[_ET | None]: ...

class EnumDecimalField(EnumField[Decimal, EnumT], Generic[EnumT]):
    """A database field supporting enumerations with Decimal values."""

    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[Decimal] | None = ...,
        max_digits: int | None = ...,
        decimal_places: int | None = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> EnumDecimalField[_ET]: ...
    @overload
    def __new__(
        cls,
        enum: type[_ET] | None = ...,
        primitive: type[Decimal] | None = ...,
        max_digits: int | None = ...,
        decimal_places: int | None = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> EnumDecimalField[_ET | None]: ...

# ---------------------------------------------------------------------------
# Flag fields
# ---------------------------------------------------------------------------

class FlagField(IntEnumField[FlagT], Generic[FlagT]):
    """
    Base class for Flag enumeration fields with bitwise-operation support.

    Values are stored two's complement in a signed column of db_bit_length
    bits so that the sign bit is usable as a flag.
    """

    @property
    def db_bit_length(self) -> int | None: ...
    @overload
    def __new__(
        cls,
        enum: type[_FT] | None = ...,
        blank: bool = ...,
        default: Any = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> FlagField[_FT]: ...
    @overload
    def __new__(
        cls,
        enum: type[_FT] | None = ...,
        blank: bool = ...,
        default: Any = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> FlagField[_FT | None]: ...

class SmallIntegerFlagField(
    FlagField[FlagT], EnumSmallIntegerField[FlagT], Generic[FlagT]
):
    """Flag field with up to 16 flags stored in a SmallIntegerField."""

class IntegerFlagField(FlagField[FlagT], EnumIntegerField[FlagT], Generic[FlagT]):
    """Flag field with up to 32 flags stored in an IntegerField."""

class BigIntegerFlagField(FlagField[FlagT], EnumBigIntegerField[FlagT], Generic[FlagT]):
    """Flag field with up to 64 flags stored in a BigIntegerField."""

class EnumExtraBigIntegerField(IntEnumField[FlagT], BinaryField, Generic[FlagT]):
    """Enum field for integers wider than 64 bits, stored as binary."""

    @overload
    def __new__(
        cls,
        enum: type[_FT] | None = ...,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> EnumExtraBigIntegerField[_FT]: ...
    @overload
    def __new__(
        cls,
        enum: type[_FT] | None = ...,
        null: Literal[True] = ...,
        **kwargs: Any,
    ) -> EnumExtraBigIntegerField[_FT | None]: ...

class ExtraBigIntegerFlagField(
    FlagField[FlagT], EnumExtraBigIntegerField[FlagT], Generic[FlagT]
):
    """Flag field for integers wider than 64 bits."""
