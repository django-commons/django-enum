"""Support for django rest framework symmetric serialization"""

__all__ = ["EnumField", "FlagField", "EnumFieldMixin"]

import inspect
from datetime import date, datetime, time, timedelta
from decimal import Decimal, DecimalException
from enum import Enum, Flag
from functools import reduce
from operator import or_
from typing import Any

from rest_framework.fields import (
    CharField,
    ChoiceField,
    DateField,
    DateTimeField,
    DecimalField,
    DurationField,
    Field,
    FloatField,
    IntegerField,
    MultipleChoiceField,
    TimeField,
)
from rest_framework.serializers import ModelSerializer
from rest_framework.utils.field_mapping import get_field_kwargs

from django_enum.fields import EnumField as EnumModelField
from django_enum.fields import FlagField as FlagModelField
from django_enum.utils import (
    choices,
    decimal_params,
    determine_primitive,
    with_typehint,
)


class ClassLookupdict:
    """
    A dict-like object that looks up values using the MRO of a class or
    instance. Similar to DRF's ClassLookupdict but returns None instead
    of raising KeyError and allows classes or object instances to be
    used as lookup keys.

    :param mapping: A dictionary containing a mapping of class types to
        values.
    """

    def __init__(self, mapping: dict[type[Any], Any]):
        self.mapping = mapping

    def __getitem__(self, key: Any) -> Any | None:
        """
        Fetch the given object for the type or type of the given object.

        :param key: An object instance or class type
        :return: The mapped value to the object instance's class or the
            passed class type. Inheritance is honored. None is returned
            if no mapping is present.
        """
        for cls in inspect.getmro(
            getattr(
                key,
                "_proxy_class",
                key if isinstance(key, type) else getattr(key, "__class__"),
            )
        ):
            if cls in self.mapping:
                return self.mapping.get(cls, None)
        return None


class EnumField(ChoiceField):
    """
    A djangorestframework serializer field for Enumeration types. If
    unspecified ModelSerializers will assign :class:`~django_enum.fields.EnumField`
    model field types to `ChoiceField
    <https://www.django-rest-framework.org/api-guide/fields/#choicefield>`_ which will
    not accept symmetrical values, this field will.

    :param enum: The type of the Enumeration of the field
    :param strict: If True (default) only values in the Enumeration type
        will be acceptable. If False, no errors will be thrown if other
        values of the same primitive type are used
    :param kwargs: Any other named arguments applicable to a ChoiceField
        will be passed up to the base classes.
    """

    enum: type[Enum]
    primitive: type[Any]
    strict: bool = True
    primitive_field: Field | None = None

    def __init__(self, enum: type[Enum], strict: bool = strict, **kwargs):
        self.enum = enum
        self.primitive = determine_primitive(enum)  # type: ignore
        assert self.primitive is not None, (
            f"Unable to determine primitive type for {enum}"
        )
        self.strict = strict
        self.choices = kwargs.pop("choices", choices(enum))
        field_name = kwargs.pop("field_name", None)
        model_field = kwargs.pop("model_field", None)
        if not self.strict:
            # if this field is not strict, we instantiate its primitive
            # field type so we can fall back to its to_internal_value
            # method if the value is not a valid enum value
            primitive_field_cls = ClassLookupdict(
                {
                    str: CharField,
                    int: IntegerField,
                    float: FloatField,
                    date: DateField,
                    datetime: DateTimeField,
                    time: TimeField,
                    timedelta: DurationField,
                    Decimal: DecimalField,
                }
            )[self.primitive]
            if primitive_field_cls:
                field_kwargs = {
                    **kwargs,
                    **{
                        key: val
                        for key, val in (
                            get_field_kwargs(field_name, model_field)
                            if field_name and model_field
                            else {}
                        ).items()
                        if key not in ["model_field", "field_name", "choices"]
                    },
                }
                if primitive_field_cls is not CharField:
                    field_kwargs.pop("allow_blank", None)
                if primitive_field_cls is DecimalField:
                    field_kwargs = {
                        **field_kwargs,
                        **decimal_params(
                            self.enum,
                            max_digits=field_kwargs.pop("max_digits", None),
                            decimal_places=field_kwargs.pop("decimal_places", None),
                        ),
                    }
                self.primitive_field = primitive_field_cls(**field_kwargs)
        super().__init__(choices=self.choices, **kwargs)

    def to_internal_value(self, data: Any) -> Enum | Any:  # type: ignore[override]
        """
        Transform the *incoming* primitive data into an enum instance.

        :return: The enum instance or the primitive value if the enum
            instance could not be found.
        """
        if data == "" and self.allow_blank:
            return ""

        if not isinstance(data, self.enum):
            try:
                data = self.enum(data)
            except (TypeError, ValueError):
                try:
                    data = self.primitive(data)
                    data = self.enum(data)
                except (TypeError, ValueError, DecimalException):
                    if self.strict:
                        self.fail("invalid_choice", input=data)
                    elif self.primitive_field:
                        return self.primitive_field.to_internal_value(data)
        return data

    def to_representation(self, value: Any) -> Any:
        """
        Transform the *outgoing* enum value into its primitive value.
        """
        return getattr(value, "value", value)


class FlagField(MultipleChoiceField):
    """
    A djangorestframework serializer field for :class:`~enum.Flag` types. If
    unspecified ModelSerializers will assign :class:`~django_enum.fields.FlagField`
    model field types to `ChoiceField
    <https://www.django-rest-framework.org/api-guide/fields/#choicefield>`_ which will
    not combine composite flag values appropriately. This field will also allow any
    symmetric values to be used (e.g. labels or names instead of values).

    **You should add** :class:`~django_enum.drf.EnumFieldMixin` **to your serializer to
    automatically use this field.**

    :param enum: The type of the flag of the field
    :param strict: If True (default) only values in the flag type
        will be acceptable. If False, no errors will be thrown if other
        values of the same primitive type are used
    :param kwargs: Any other named arguments applicable to a ChoiceField
        will be passed up to the base classes.
    """

    enum: type[Flag]
    strict: bool = True

    def __init__(self, enum: type[Flag], strict: bool = strict, **kwargs):
        self.enum = enum
        self.strict = strict
        self.choices = kwargs.pop("choices", choices(enum))
        kwargs.pop("field_name", None)
        kwargs.pop("model_field", None)
        super().__init__(choices=self.choices, **kwargs)

    def to_internal_value(self, data: Any) -> Enum | Any:  # type: ignore[override]
        """
        Transform the *incoming* primitive data into an enum instance.
        We accept a composite flag value or a list of values. If a list,
        each element will be converted to a flag value and then the values
        will be reduced into a composite value with the or operator.

        :return: A composite flag value.
        """
        if not data:
            if self.allow_null and (data is None or data == ""):
                return None
            return self.enum(0)

        if not isinstance(data, self.enum):
            try:
                return self.enum(data)
            except (TypeError, ValueError):
                try:
                    if isinstance(data, str):
                        return self.enum[data]
                    if isinstance(data, (list, tuple)):
                        values = []
                        for val in data:
                            try:
                                values.append(self.enum(val))
                            except (TypeError, ValueError):
                                values.append(self.enum[val])
                        return reduce(or_, values)
                except (TypeError, ValueError, KeyError):
                    pass
                self.fail("invalid_choice", input=data)
        return data

    def to_representation(self, value: Any) -> Any:
        """
        Transform the *outgoing* enum value into its primitive value.

        :return: The primitive composite value of the flag (most likely an integer).
        """
        return getattr(value, "value", value)


class EnumFieldMixin(with_typehint(ModelSerializer)):  # type: ignore
    """
    A mixin for ModelSerializers that adds auto-magic support for
    EnumFields.
    """

    def build_standard_field(
        self, field_name: str, model_field: EnumModelField
    ) -> tuple[type[Field], dict[str, Any]]:
        """
        The default implementation of build_standard_field will set any
        field with choices to a ChoiceField. This will override that for
        EnumFields and add enum and strict arguments to the field's kwargs.

        To use this mixin, include it before ModelSerializer in your
        serializer's class hierarchy:

        .. code-block:: python

            from django_enum.drf import EnumFieldMixin
            from rest_framework.serializers import ModelSerializer

            class MySerializer(EnumFieldMixin, ModelSerializer):

                class Meta:
                    model = MyModel
                    fields = '__all__'


        :param field_name: The name of the field on the serializer
        :param model_field: The Field instance on the model
        :return: A 2-tuple, the first element is the field class, the
            second is the kwargs for the field
        """
        field_class = ClassLookupdict(
            {FlagModelField: FlagField, EnumModelField: EnumField}
        )[model_field]
        if field_class:
            return field_class, {
                "enum": model_field.enum,
                "strict": model_field.strict,
                "field_name": field_name,
                "model_field": model_field,
                **super().build_standard_field(field_name, model_field)[1],
            }
        return super().build_standard_field(field_name, model_field)
