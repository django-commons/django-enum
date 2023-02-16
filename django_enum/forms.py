"""Enumeration support for django model forms"""
from typing import Any, Iterable, List, Optional, Tuple, Type, Union

from django.core.exceptions import ValidationError
from django.db.models import Choices
from django.forms.fields import TypedChoiceField, TypedMultipleChoiceField
from django.forms.widgets import Select, SelectMultiple

__all__ = [
    'NonStrictSelect',
    'NonStrictSelectMultiple',
    'FlagSelectMultiple',
    'EnumChoiceField',
    'EnumFlagField'
]


class _Unspecified:
    """
    Marker used by EnumChoiceField to determine if empty_value
    was overridden
    """


class NonStrictMixin:

    choices: Iterable[Tuple[Any, str]]

    def render(self, *args, **kwargs):
        """
        Before rendering if we're a non-strict field and our value is not
        one of our choices, we add it as an option.
        """

        value: Any = getattr(kwargs.get('value'), 'value', kwargs.get('value'))
        if (
            value not in EnumChoiceField.empty_values
            and value not in (
                choice[0] for choice in self.choices
            )
        ):
            self.choices = list(self.choices) + [(value, str(value))]
        return super().render(*args, **kwargs)


class NonStrictSelect(NonStrictMixin, Select):
    """
    A Select widget for non-strict EnumChoiceFields that includes any existing
    non-conforming value as a choice option.
    """


class FlagSelectMultiple(SelectMultiple):
    pass


class NonStrictSelectMultiple(NonStrictMixin, SelectMultiple):
    """
    A SelectMultiple widget for non-strict EnumFlagFields that includes any
    existing non-conforming value as a choice option.
    """


class ChoiceFieldMixin:
    """
    Mixin to adapt base model form ChoiceFields to use on EnumFields.

    :param enum: The Enumeration type
    :param empty_value: Allow users to define what empty is because some
        enumeration types might use an empty value (i.e. empty string) as an
        enumeration value. This value will be returned when any "empty" value
        is encountered. If unspecified the default empty value of '' is
        returned.
    :param empty_values: Override the list of what are considered to be empty
        values.
    :param strict: If False, values not included in the enumeration list, but
        of the same primitive type are acceptable.
    :param choices: Override choices, otherwise enumeration choices attribute
        will be used.
    :param kwargs: Any additional parameters to pass to ChoiceField base class.
    """

    enum_: Optional[Type[Choices]] = None
    strict_: bool = True
    empty_value: Any = ''
    empty_values: List[Any]
    choices: Iterable[Tuple[Any, Any]]

    def __init__(
            self,
            enum: Optional[Type[Choices]] = None,
            *,
            empty_value: Any = _Unspecified,
            strict: bool = strict_,
            empty_values: List[Any] = TypedChoiceField.empty_values,
            choices: Iterable[Tuple[Any, str]] = (),
            **kwargs
    ):
        self.strict = strict
        if not self.strict:
            kwargs.setdefault('widget', NonStrictSelect)

        self.empty_values = empty_values

        super().__init__(
            choices=choices or getattr(self.enum, 'choices', choices),
            coerce=kwargs.pop('coerce', self.coerce),
            **kwargs
        )

        if empty_value is not _Unspecified:
            if empty_value not in self.empty_values:
                self.empty_values.insert(0, empty_value)
            self.empty_value = empty_value

        if enum:
            self.enum = enum

    @property
    def strict(self):
        """strict fields allow non-enumeration values"""
        return self.strict_

    @strict.setter
    def strict(self, strict):
        self.strict_ = strict

    @property
    def enum(self):
        """the class of the enumeration"""
        return self.enum_

    @enum.setter
    def enum(self, enum):
        self.enum_ = enum
        self.choices = self.choices or getattr(
            self.enum,
            'choices',
            self.choices
        )
        # remove any of our valid enumeration values or symmetric properties
        # from our empty value list if there exists an equivalency
        for empty in self.empty_values:
            for enum_val in self.enum:
                if empty == enum_val:
                    # copy the list instead of modifying the class's
                    self.empty_values = [
                        empty for empty in self.empty_values
                        if empty != enum_val
                    ]
                    if empty == self.empty_value:
                        if self.empty_values:
                            self.empty_value = self.empty_values[0]
                        else:
                            raise ValueError(
                                f'Enumeration value {repr(enum_val)} is'
                                f'equivalent to {self.empty_value}, you must '
                                f'specify a non-conflicting empty_value.'
                            )

    def _coerce_to_value_type(self, value: Any) -> Any:
        """Coerce the value to the enumerations value type"""
        return type(self.enum.values[0])(value)

    def prepare_value(self, value: Any) -> Any:
        """Must return the raw enumeration value type"""
        value = self._coerce(value)
        return super().prepare_value(
            value.value
            if isinstance(value, self.enum)
            else value
        )

    def to_python(self, value: Any) -> Union[Choices, Any]:
        """Return the value as its full enumeration object"""
        return self._coerce(value)

    def valid_value(self, value: Any) -> bool:
        """Return false if this value is not valid"""
        try:
            self._coerce(value)
            return True
        except ValidationError:
            return False

    def coerce(  # pylint: disable=E0202
            self, value: Any
    ) -> Union[Choices, Any]:
        """
        Attempt conversion of value to an enumeration value and return it
        if successful.

        .. note::

            When used to represent a model field, by default the model field's
            to_python method will be substituted for this method.

        :param value: The value to convert
        :raises ValidationError: if a valid return value cannot be determined.
        :return: An enumeration value or the canonical empty value if value is
            one of our empty_values, or the value itself if this is a
            non-strict field and the value is of a matching primitive type
        """
        if (
            self.enum is not None and
            not isinstance(value, self.enum)  # pylint: disable=R0801
        ):
            try:
                value = self.enum(value)
            except (TypeError, ValueError):
                try:
                    value = self._coerce_to_value_type(value)
                    value = self.enum(value)
                except (TypeError, ValueError) as err:
                    if self.strict or not isinstance(
                        value,
                        type(self.enum.values[0])
                    ):
                        raise ValidationError(
                            f'{value} is not a valid {self.enum}.',
                            code='invalid_choice',
                            params={'value': value},
                        ) from err
        return value


class EnumChoiceField(ChoiceFieldMixin, TypedChoiceField):
    """
    The default ``ChoiceField`` will only accept the base enumeration values.
    Use this field on forms to accept any value mappable to an enumeration
    including any labels or symmetric properties.
    """


class EnumFlagField(ChoiceFieldMixin, TypedMultipleChoiceField):
    """
    The default ``TypedMultipleChoiceField`` will only accept the base
    enumeration values. Use this field on forms to accept any value mappable
    to an enumeration including any labels or symmetric properties.

    Behavior:

    if no select value in post data:
        if null=True, no choice is null.
        If null=False, no choice is Enum(0)
    if select value in post data:
        if null=True or False, no choice is Enum(0)

    if strict=False, values can be outside of the enumerations
    """

    def __init__(
            self,
            enum: Optional[Type[Choices]] = None,
            *,
            empty_value: Any = _Unspecified,
            strict: bool = ChoiceFieldMixin.strict_,
            empty_values: List[Any] = TypedChoiceField.empty_values,
            choices: Iterable[Tuple[Any, str]] = (),
            **kwargs
    ):
        super().__init__(
            enum=enum,
            empty_value=(
                enum(0) if enum and empty_value is _Unspecified
                else empty_value
            ),
            strict=strict,
            empty_values=empty_values,
            choices=choices,
            **kwargs
        )
