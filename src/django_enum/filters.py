"""
Support for :doc:`django-filter <django-filter:index>`.
"""

from __future__ import annotations

import typing as t
from enum import Enum, Flag

from django.db.models import Field as ModelField
from django.db.models import Q
from django_filters import filterset
from django_filters.filters import Filter, TypedChoiceFilter, TypedMultipleChoiceFilter
from django_filters.utils import try_dbfield

from django_enum.fields import EnumField, FlagField
from django_enum.forms import EnumChoiceField, EnumFlagField, EnumMultipleChoiceField
from django_enum.utils import choices

__all__ = [
    "EnumFilter",
    "MultipleEnumFilter",
    "EnumFlagFilter",
    "FilterSet",
]


class EnumFilter(TypedChoiceFilter):
    """
    Use this filter class instead of :class:`~django_filters.filters.ChoiceFilter`
    to get filters to accept :class:`~enum.Enum` labels and symmetric properties.

    For example if we have an enumeration field defined with the following
    Enum:

    .. code-block:: python

        class Color(TextChoices):

            rgb: Annotated[Tuple[int, int, int], Symmetric()]
            hex: Annotated[str, Symmetric(case_fold=True)]

            RED   = 'R', 'Red',   (1, 0, 0), 'ff0000'
            GREEN = 'G', 'Green', (0, 1, 0), '00ff00'
            BLUE  = 'B', 'Blue',  (0, 0, 1), '0000ff'

        color = EnumField(Color)

    The default :class:`~django_filters.filters.ChoiceFilter` will only work with
    the enumeration values: ?color=R, ?color=G, ?color=B. ``EnumFilter`` will accept
    query parameter values from any of the symmetric properties: ?color=Red,
    ?color=ff0000, etc...

    :param enum: The class of the enumeration containing the values to
        filter on
    :param strict: If False (default), values not in the enumeration will
        be searchable.
    :param kwargs: Any additional arguments from the base classes
        (:class:`~django_filters.filters.TypedChoiceFilter`)
    """

    enum: type[Enum]
    strict: bool
    field_class = EnumChoiceField

    def __init__(self, *, enum: type[Enum], strict: bool = True, **kwargs):
        self.enum = enum
        self.strict = strict
        super().__init__(
            enum=enum,
            strict=strict,
            choices=kwargs.pop("choices", choices(self.enum)),
            **kwargs,
        )


class MultipleEnumFilter(TypedMultipleChoiceFilter):
    """
    Use this filter class instead of
    :class:`~django_filters.filters.MultipleChoiceFilter` to get filters to accept
    multiple :class:`~enum.Enum` labels and symmetric properties.

    :param enum: The class of the enumeration containing the values to
        filter on
    :param strict: If False (default), values not in the enumeration will
        be searchable.
    :param conjoined: If True require all values to be present, if False require any
    :param kwargs: Any additional arguments from base classes,
        (:class:`~django_filters.filters.TypedMultipleChoiceFilter`)
    """

    enum: type[Enum]
    strict: bool
    field_class = EnumMultipleChoiceField

    def __init__(
        self,
        *,
        enum: type[Enum],
        strict: bool = True,
        conjoined: bool = False,
        **kwargs,
    ):
        self.enum = enum
        self.strict = strict
        super().__init__(
            enum=enum,
            strict=strict,
            choices=kwargs.pop("choices", choices(self.enum)),
            conjoined=conjoined,
            **kwargs,
        )


class EnumFlagFilter(TypedMultipleChoiceFilter):
    """
    Use this filter class with :class:`~django_enum.fields.FlagField` fields. It will
    allow the field to be listed multiple times in URL query strings
    (e.g. ``field=value&field=value``). By default the filter will query on these values with
    :ref:`has_any` these values together. Use ``conjoined`` to use :ref:`has_all` instead.

    This filter also respects the :class:`~django_filters.filters.TypedMultipleChoiceFilter`
    base class parameters such as ``exclude``.

    :param enum: The class of the enumeration containing the values to
        filter on
    :param strict: If False (default), values not in the enumeration will
        be searchable.
    :param conjoined: If True use :ref:`has_all` lookup, otherwise use :ref:`has_any`
        (default)
    :param kwargs: Any additional arguments from base classes,
        (:class:`~django_filters.filters.TypedMultipleChoiceFilter`)
    """

    enum: type[Flag]
    field_class = EnumFlagField

    parent: FilterSet | None = None

    def __init__(
        self,
        *,
        enum: type[Flag],
        strict: bool = True,
        conjoined: bool = False,
        **kwargs,
    ):
        self.enum = enum
        super().__init__(
            enum=enum,
            choices=kwargs.pop("choices", choices(self.enum)),
            strict=strict,
            conjoined=conjoined,
            **kwargs,
        )
        self.lookup_expr = "has_all" if conjoined else "has_any"

    def is_noop(self, qs, value):
        return value is None or value == ""

    def filter(self, qs, value):
        if self.is_noop(qs, value):
            return qs

        # special case of no activate flags, performs an exact lookup
        # the form cleans unsupplied fields into 0s so we make sure this was supplied
        # before filtering on it
        if not value:
            if not self.parent or self.field_name in self.parent.form.data:
                return self.get_method(qs)(Q(**{f"{self.field_name}": 0}))
            return qs

        qs = self.get_method(qs)(Q(**self.get_filter_predicate(value)))  # type: ignore
        return qs.distinct() if self.distinct else qs


class FilterSet(filterset.FilterSet):
    """
    This filterset behaves the same way as the :doc:`django-filter <django-filter:index>`
    :class:`~django_filters.filterset.FilterSet` except the following fields will be set
    to the following filter types:

    * :class:`~django_enum.fields.EnumField` -> :class:`~django_enum.filters.EnumFilter`
    * :class:`~django_enum.fields.FlagField` -> :class:`~django_enum.filters.FlagFilter`

    **If you have a custom** :class:`~django_filters.filterset.FilterSet`
    **implementation, this class can also be used as a mixin.**
    """

    @staticmethod
    def enum_extra(f: EnumField) -> dict[str, t.Any]:
        return {"enum": f.enum, "strict": f.strict, "choices": f.choices}

    FILTER_DEFAULTS = {
        **{
            FlagField: {
                "filter_class": EnumFlagFilter,
                "extra": lambda f: FilterSet.enum_extra(f),  # TODO 3.9 compat
            },
            EnumField: {
                "filter_class": EnumFilter,
                "extra": lambda f: FilterSet.enum_extra(f),  # TODO 3.9 compat
            },
        },
        **filterset.FilterSet.FILTER_DEFAULTS,
    }

    @classmethod
    def filter_for_lookup(
        cls, field: ModelField, lookup_type: str
    ) -> tuple[type[Filter], dict[str, t.Any]]:
        """For EnumFields use the EnumFilter class by default"""
        # we can't just pass this up to the base implementation because if it sees
        # choices on a field it will hard set to ChoiceField
        if isinstance(field, EnumField):
            data = (
                try_dbfield(
                    {
                        **cls.FILTER_DEFAULTS,
                        **(
                            getattr(getattr(cls, "_meta", None), "filter_overrides", {})
                        ),
                    }.get,
                    field.__class__,
                )
                or {}
            )
            return (
                data["filter_class"],
                {
                    **FilterSet.enum_extra(field),
                    **data.get("extra", lambda f: {})(field),
                },
            )
        return super().filter_for_lookup(field, lookup_type)
