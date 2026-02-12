"""Enumeration support for django model forms"""

import typing as t
from copy import copy
from decimal import DecimalException
from enum import Enum, Flag
from functools import reduce
from operator import or_

from django.core.exceptions import ValidationError
from django.forms.fields import (
    Field,
    TypedChoiceField,
    TypedMultipleChoiceField,
)
from django.forms.widgets import (
    CheckboxSelectMultiple,
    ChoiceWidget,
    RadioSelect,
    Select,
    SelectMultiple,
)

from django_enum.utils import choices as get_choices
from django_enum.utils import (
    decompose,
    determine_primitive,
    get_set_bits,
    get_set_values,
    with_typehint,
)

__all__ = [
    "NonStrictSelect",
    "NonStrictSelectMultiple",
    "FlagSelectMultiple",
    "FlagCheckbox",
    "NonStrictFlagSelectMultiple",
    "NonStrictFlagCheckbox",
    "NonStrictRadioSelect",
    "ChoiceFieldMixin",
    "EnumChoiceField",
    "EnumMultipleChoiceField",
    "EnumFlagField",
    "NonStrictMixin",
    "FlagMixin",
    "NonStrictFlagMixin",
]


_SelectChoices = t.Iterable[
    tuple[t.Any, t.Any] | tuple[str, t.Iterable[tuple[t.Any, t.Any]]]
]

_Choice = tuple[t.Any, t.Any]
_ChoiceNamedGroup = tuple[str, t.Iterable[_Choice]]
_FieldChoices = t.Iterable[_Choice | _ChoiceNamedGroup]


class _ChoicesCallable(t.Protocol):
    def __call__(self) -> _FieldChoices: ...  # pragma: no cover


_ChoicesParameter = _FieldChoices | _ChoicesCallable


class _CoerceCallable(t.Protocol):
    def __call__(self, value: t.Any, /) -> t.Any: ...  # pragma: no cover


class _Unspecified:
    """
    Marker used by EnumChoiceField to determine if empty_value
    was overridden
    """


class NonStrictMixin:
    """
    Mixin to add non-strict behavior to a widget, this makes sure the set value
    appears as a choice if it is not one of the enumeration choices.
    """

    choices: _SelectChoices

    def render(self, *args, **kwargs):
        """
        Before rendering if we're a non-strict field and our value is not
        one of our choices, we add it as an option.
        """

        value: t.Any = getattr(kwargs.get("value"), "value", kwargs.get("value"))
        if value not in EnumChoiceField.empty_values and value not in (
            choice[0] for choice in self.choices
        ):
            self.choices = list(self.choices) + [(value, str(value))]
        return super().render(*args, **kwargs)  # type: ignore[misc]


class NonStrictFlagMixin:
    """
    Mixin to add non-strict behavior to a multiple choice flag widget, this makes sure
    that set flags outside of the enumerated flags will show up as choices. They will
    be displayed as the index of the set bit.
    """

    choices: _SelectChoices

    def render(self, *args, **kwargs):
        """
        Before rendering if we're a non-strict flag field and bits are set that are
        not part of our flag enumeration we add them as (integer value, bit index)
        to our (value, label) choice list.
        """

        raw_choices = zip(
            get_set_values(kwargs.get("value")), get_set_bits(kwargs.get("value"))
        )
        self.choices = list(self.choices)
        choice_values = set(choice[0] for choice in self.choices)
        for value, label in raw_choices:
            if value not in choice_values:
                self.choices.append((value, label))
        return super().render(*args, **kwargs)  # type: ignore[misc]


class NonStrictSelect(NonStrictMixin, Select):
    """
    **This is the default widget used for** :class:`~django_enum.fields.EnumField`
    **fields that have** ``strict`` **set to** ``False``.

    This widget will render a drop down select field that includes an option for each
    value on the enumeration, but if the field is set to a value outside of the
    enumeration it will be included and selected in the drop down:

    For example, using our :ref:`Color <color_ex>` enumeration:

    .. code-block:: python

        class Model(models.Model):
            color = EnumField(Color, strict=False, max_length=12)

        Model.objects.create(color="YELLOW")

    .. image:: ../widgets/NonStrictSelect.png
    """


class NonStrictRadioSelect(NonStrictMixin, RadioSelect):
    """
    This widget will render a radio button select field that includes an option for each
    value on the enumeration, but if the field is set to a value outside of the
    enumeration it will be included and selected:

    For example, using our :ref:`Color <color_ex>` enumeration:

    .. code-block:: python

        class Model(models.Model):
            color = EnumField(Color, strict=False, max_length=12)

        Model.objects.create(color="YELLOW")

    .. image:: ../widgets/NonStrictRadioSelect.png
    """


class FlagMixin:
    """
    This mixin adapts a widget to work with :class:`~enum.IntFlag` types.
    """

    enum: type[Flag] | None

    def __init__(self, enum: type[Flag] | None = None, **kwargs):
        self.enum = enum
        super().__init__(**kwargs)

    def format_value(self, value):
        """
        Return a list of the flag's values, unpacking it if necessary.
        """
        if value is None:
            return []
        if not isinstance(value, list):
            # see impl of ChoiceWidget.optgroups
            # it compares the string conversion of the value of each
            # choice tuple to the string conversion of the value
            # to determine selected options
            if self.enum:
                named = [str(en.value) for en in decompose(self.enum(value))]
                named_set = set(named)
                unnamed = [
                    str(val)
                    for val in get_set_values(value)
                    if str(val) not in named_set
                ]
                return [*named, *unnamed]
            if isinstance(value, int):
                # automagically work for IntFlags even if we weren't given the enum
                return [str(val) for val in get_set_values(value)]
        return value


class FlagSelectMultiple(FlagMixin, SelectMultiple):
    """
    **This is the default widget used for** :class:`~django_enum.fields.FlagField`
    **fields.**

    This widget will render :class:`~enum.IntFlag` types as a multi select field with
    an option for each flag value. Values outside of the enumeration will not be
    displayed.

    For example, using our :ref:`Permissions <permissions_ex>` enumeration:

    .. code-block:: python

        class Model(models.Model):
            permissions = EnumField(Permissions)

        Model.objects.create(permissions=Permissions.READ | Permissions.EXECUTE)

    .. image:: ../widgets/FlagSelectMultiple.png
    """


class FlagCheckbox(FlagMixin, CheckboxSelectMultiple):
    """
    This widget will render :class:`~enum.IntFlag` types as checkboxes with a checkbox
    for each flag value.

    For example, using our :ref:`Permissions <permissions_ex>` enumeration:

    .. code-block:: python

        class Model(models.Model):
            permissions = EnumField(Permissions)

        Model.objects.create(permissions=Permissions.READ | Permissions.EXECUTE)

    .. image:: ../widgets/FlagCheckbox.png
    """


class NonStrictSelectMultiple(NonStrictMixin, SelectMultiple):
    """
    This widget will render a multi select box that includes an option for each
    value on the enumeration and for any non-value that is passed in.
    """


class NonStrictFlagSelectMultiple(NonStrictFlagMixin, FlagSelectMultiple):
    """
    This widget will render a multi select box that includes an option for each flag
    on the enumeration and also for each bit lot listed in the enumeration that is set
    on the value.

    Options for extra bits only appear if they are set. You should pass choices to the
    form field if you want additional options to always appear.

    .. code-block:: python

        class Model(models.Model):
            permissions = EnumField(Permissions, strict=False)

        Model.objects.create(
            permissions=Permissions.READ | Permissions.EXECUTE | ( 1 << 4 )
        )

    .. image:: ../widgets/NonStrictFlagSelectMultiple.png
    """


class NonStrictFlagCheckbox(NonStrictFlagMixin, FlagCheckbox):
    """
    This widget will render a checkbox for each flag on the enumeration and also
    for each bit not listed in the enumeration that is set on the value.

    Checkboxes for extra bits only appear if they are set. You should pass choices to
    the form field if you want additional checkboxes to always appear.

    For example, using our :ref:`Permissions <permissions_ex>` enumeration:

    .. code-block:: python

        class Model(models.Model):
            permissions = EnumField(Permissions, strict=False)

        Model.objects.create(
            permissions=Permissions.READ | Permissions.EXECUTE | ( 1 << 4 )
        )

    .. image:: ../widgets/NonStrictFlagCheckbox.png
    """


class ChoiceFieldMixin(
    with_typehint(TypedChoiceField)  # type: ignore
):
    """
    Mixin to adapt :class:`django.forms.ChoiceField` to use with
    :class:`~django_enum.fields.EnumField`.

    :param enum: The Enumeration type
    :param empty_value: Allow users to define what empty is because some
        enumeration types might use an empty value (i.e. empty string) as an
        enumeration value. This value will be returned when any "empty" value
        is encountered. If unspecified the default empty value of '' is
        returned.
    :param empty_values: Override the list of what are considered to be empty
        values. Defaults to TypedChoiceField.empty_values.
    :param strict: If False, values not included in the enumeration list, but
        of the same primitive type are acceptable.
    :param choices: Override choices, otherwise enumeration choices attribute
        will be used.
    :param kwargs: Any additional parameters to pass to ChoiceField base class.
    """

    _enum_: type[Enum] | None = None
    _primitive_: type | None = None
    _strict_: bool = True
    empty_value: t.Any = ""
    empty_values: t.Sequence[t.Any] = list(TypedChoiceField.empty_values)

    _empty_value_overridden_: bool = False
    _empty_values_overridden_: bool = False

    choices: _ChoicesParameter

    non_strict_widget: type[ChoiceWidget] | None = NonStrictSelect

    def __init__(
        self,
        enum: type[Enum] | None = _enum_,
        primitive: type | None = _primitive_,
        *,
        empty_value: t.Any = _Unspecified,
        strict: bool = _strict_,
        empty_values: list[t.Any] | type[_Unspecified] = _Unspecified,
        choices: _ChoicesParameter = (),
        coerce: _CoerceCallable | None = None,
        **kwargs,
    ):
        self._strict_ = strict
        self._primitive_ = primitive
        if not self.strict and self.non_strict_widget:
            kwargs.setdefault("widget", self.non_strict_widget)

        if empty_values is _Unspecified:
            self.empty_values = copy(list(TypedChoiceField.empty_values))
        else:
            assert isinstance(empty_values, list)
            self.empty_values = empty_values
            self._empty_values_overridden_ = True

        super().__init__(
            choices=choices or getattr(self.enum, "choices", choices),
            coerce=coerce or self.default_coerce,
            **kwargs,
        )

        if empty_value is not _Unspecified:
            self._empty_value_overridden_ = True
            if (
                empty_value not in self.empty_values
                and not self._empty_values_overridden_
            ):
                self.empty_values = [empty_value, *self.empty_values]
            self.empty_value = empty_value

        if enum:
            self.enum = enum

    @property
    def strict(self):
        """strict fields allow non-enumeration values"""
        return self._strict_

    @strict.setter
    def strict(self, strict):
        self._strict_ = strict

    @property
    def primitive(self):
        """
        The most appropriate primitive non-Enumeration type that can represent
        all enumeration values.
        """
        return self._primitive_

    @primitive.setter
    def primitive(self, primitive):
        self._primitive_ = primitive

    @property
    def enum(self):
        """the class of the enumeration"""
        return self._enum_

    @enum.setter
    def enum(self, enum):
        self._enum_ = enum
        self._primitive_ = self._primitive_ or determine_primitive(enum)
        self.choices = self.choices or get_choices(self.enum)
        # remove any of our valid enumeration values or symmetric properties
        # from our empty value list if there exists an equivalency
        if not self._empty_values_overridden_:
            members = self.enum.__members__.values()
            self.empty_values = [val for val in self.empty_values if val not in members]
        if (
            not self._empty_value_overridden_
            and self.empty_value not in self.empty_values
            and self.empty_values
        ):
            self.empty_value = self.empty_values[0]

        if self.empty_value not in self.empty_values:
            raise ValueError(
                f"Enumeration value {repr(self.empty_value)} is"
                f"equivalent to {self.empty_value}, you must "
                f"specify a non-conflicting empty_value."
            )

    def _coerce_to_value_type(self, value: t.Any) -> t.Any:
        """Coerce the value to the enumerations value type"""
        return self.primitive(value) if self.primitive else value

    def prepare_value(self, value: t.Any) -> t.Any:
        """Must return the raw enumeration value type"""
        value = self._coerce(value)  # type: ignore
        return super().prepare_value(
            value.value if self.enum and isinstance(value, self.enum) else value
        )

    def to_python(self, value: t.Any) -> t.Any:
        """Return the value as its full enumeration object"""
        return self._coerce(value)  # type: ignore

    def valid_value(self, value: t.Any) -> bool:
        """Return false if this value is not valid"""
        try:
            self._coerce(value)  # type: ignore
            return True
        except ValidationError:
            return False

    def default_coerce(self, value: t.Any) -> t.Any:
        """
        Attempt conversion of value to an enumeration value and return it
        if successful.

        .. note::

            When used to represent a model field, by default the model field's
            to_python method will be substituted for this method.

        :param value: The value to convert
        :raises ValidationError: if a valid return value cannot be determined.
        :returns: An enumeration value or the canonical empty value if value is
            one of our empty_values, or the value itself if this is a
            non-strict field and the value is of a matching primitive type
        """
        if self.enum is not None and not isinstance(value, self.enum):
            try:
                value = self.enum(value)
            except (TypeError, ValueError):
                try:
                    value = self._coerce_to_value_type(value)
                    value = self.enum(value)
                except (TypeError, ValueError, DecimalException):
                    try:
                        value = self.enum[value]
                    except KeyError as err:
                        assert self.primitive
                        if self.strict or not isinstance(value, self.primitive):
                            raise ValidationError(
                                f"{value} is not a valid {self.enum}.",
                                code="invalid_choice",
                                params={"value": value},
                            ) from err
        return value

    def validate(self, value):
        """Validate that the input is in self.choices."""
        # there is a bug in choice field where it passes 0 values, we skip over
        # its implementation and call the parent class's validate
        Field.validate(self, value)
        if value not in self.empty_values and not self.valid_value(value):
            raise ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": value},
            )


class EnumChoiceField(ChoiceFieldMixin, TypedChoiceField):  # type: ignore
    """
    The default :class:`~django.forms.ChoiceField` will only accept the base
    enumeration values. Use this field on forms to accept any value mappable to an
    enumeration including any labels, symmetric properties, of values accepted in
    :meth:`~enum.Enum._missing_`.

    .. tip::

        See :class:`~django_enum.forms.ChoiceFieldMixin` for the list of parameters accepted by the
        form fields. These parameters mirror the parameters for :class:`~django_enum.fields.EnumField`.
    """


class EnumMultipleChoiceField(  # type: ignore
    ChoiceFieldMixin, TypedMultipleChoiceField
):
    """
    The default :class:`~django.forms.MultipleChoiceField` will only accept the
    base enumeration values. Use this field on forms to accept multiple values mappable
    to an enumeration including any labels, symmetric properties, of values accepted in
    :meth:`~enum.Enum._missing_`.
    """

    non_strict_widget = NonStrictSelectMultiple

    def has_changed(self, initial, data):
        return super().has_changed(
            *(
                [
                    (str(en.value) if isinstance(en, Enum) else en)
                    for en in initial or []
                ],
                [(str(en.value) if isinstance(en, Enum) else en) for en in data or []],
            )
        )


class EnumFlagField(ChoiceFieldMixin, TypedMultipleChoiceField):  # type: ignore
    """
    A generic form field for :class:`~enum.Flag` derived enumerations. By default the
    :class:`~django_enum.forms.FlagSelectMultiple` widget will be used.

    After cleaning the value stored in the cleaned data will be a combined enum
    instance. (e.g. all input flags will be or-ed together)

    .. note::

        The default empty_value is Flag(0) but when used in a ModelForm the empty_value
        will be automatically set to None if null=True.
    """

    widget = FlagSelectMultiple
    non_strict_widget = NonStrictFlagSelectMultiple

    def __init__(
        self,
        enum: type[Flag] | None = None,
        *,
        empty_value: t.Any = _Unspecified,
        strict: bool = ChoiceFieldMixin._strict_,
        empty_values: list[t.Any] | type[_Unspecified] = _Unspecified,
        choices: _ChoicesParameter = (),
        **kwargs,
    ):
        widget = kwargs.get("widget", self.widget if strict else self.non_strict_widget)
        if isinstance(widget, type) and issubclass(widget, FlagMixin):
            widget = widget(enum=enum)
        kwargs["widget"] = widget
        super().__init__(
            enum=enum,
            empty_value=(
                enum(0) if enum and empty_value is _Unspecified else empty_value
            ),
            strict=strict,
            empty_values=empty_values,
            choices=choices,
            **kwargs,
        )

    def _coerce(self, value: t.Any) -> t.Any:
        """Combine the values into a single flag using |"""
        if self.enum and isinstance(value, self.enum):
            return value
        values = TypedMultipleChoiceField._coerce(  # type: ignore[attr-defined]
            self, [value] if value and not isinstance(value, list) else value
        )
        if values:
            return reduce(or_, values)
        return self.empty_value

    def has_changed(self, initial, data):
        return super().has_changed(
            *(
                [str(v) for v in get_set_values(initial)]
                if isinstance(initial, int)
                else [str(en.value) for en in decompose(initial)]
                if isinstance(initial, Flag)
                else initial,
                [str(v) for v in get_set_values(data)]
                if isinstance(data, int)
                else [str(en.value) for en in decompose(data)]
                if isinstance(data, Flag)
                else data,
            )
        )
