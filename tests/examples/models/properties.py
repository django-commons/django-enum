# flake8: noqa
import typing as t
from django.db import models
from enum_properties import Symmetric, StrEnumProperties
from django_enum import EnumField


class PropertyExample(models.Model):

    class Color(StrEnumProperties):

        label: str
        rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
        hex: t.Annotated[str, Symmetric(case_fold=True)]

        # fmt: off
        # name value label       rgb       hex
        RED   = "R", "Red",   (1, 0, 0), "ff0000"
        GREEN = "G", "Green", (0, 1, 0), "00ff00"
        BLUE  = "B", "Blue",  (0, 0, 1), "0000ff"
        # fmt: on

        # any type hints before the values in the Enum's definition become
        # properties on each value, and the enumeration value may be
        # instantiated from any symmetric property's value

    color = EnumField(Color)
