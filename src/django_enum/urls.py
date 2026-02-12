"""
A metaclass and converter for Django's URL dispatcher to use with Python's
Enum class.
"""

from enum import Enum

from django.urls.converters import register_converter

from django_enum.utils import determine_primitive

__all__ = ["register_enum_converter"]


class _EnumConverter:
    enum: type[Enum]
    prop: str = "value"
    primitive: type

    regex: str = ".+"

    _lookup_: dict[str, Enum]

    def to_python(self, value: str) -> Enum:
        """
        Convert the string representation of the enum into an instance of it.
        """
        return self._lookup_[value]

    def to_url(self, value: Enum) -> str:
        """
        Convert the given enumeration value to its url string.

        :param value: The enumeration value
        :return: the string representation of the enumeration value
        """
        return str(getattr(value, self.prop))


def register_enum_converter(enum: type[Enum], type_name="", prop="value"):
    """
    Register an enum converter for Django's URL dispatcher.

    :param enum: The enumeration type to register.
    :param type_name: the name to use for the converter, defaults to the enum class
        name:

        .. code-block:: python

            path("<type_name:kwarg_name>", view, view_name)

    :param prop: The property name to use in the urls - by default the value is used.
    """
    register_converter(
        type(
            f"{enum.__name__}Converter",
            (_EnumConverter,),
            {
                "enum": enum,
                "prop": prop,
                "primitive": determine_primitive(enum),
                "regex": "|".join([str(getattr(env, prop)) for env in enum]),
                "_lookup_": {str(getattr(env, prop)): env for env in enum},
            },
        ),
        type_name or enum.__name__,
    )
