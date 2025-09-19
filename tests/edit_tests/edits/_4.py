import typing as t

from django.db import models
from enum_properties import Symmetric

from django_enum import EnumField
from django_enum.choices import TextChoices


class MigrationTester(models.Model):
    # unchanged
    class IntEnum(models.IntegerChoices):
        ONE = 1, "One"
        TWO = (
            2,
            "Two",
        )
        THREE = 3, "Three"

    # change enumeration names
    class Color(TextChoices):
        rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
        hex: t.Annotated[str, Symmetric(case_fold=True)]

        # name   value   label       rgb       hex
        RD = "R", "Red", (1, 0, 0), "ff0000"
        GR = "G", "Green", (0, 1, 0), "00ff00"
        BL = "B", "Blue", (0, 0, 1), "0000ff"

    # change strict and leave constrain on - should not generate a migration
    int_enum = EnumField(IntEnum, strict=False, constrained=True)
    color = EnumField(Color)
