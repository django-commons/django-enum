import typing as t

from django.db import models
from enum_properties import Symmetric

from django_enum import EnumField
from django_enum.choices import TextChoices


class MigrationTester(models.Model):
    class IntEnum(models.TextChoices):
        A = "A", "One"
        B = (
            "B",
            "Two",
        )
        C = "C", "Three"

    class Color(TextChoices):
        rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
        hex: t.Annotated[str, Symmetric(case_fold=True)]

        RED = "R", "Red", (1, 0, 0), "ff0000"
        GREEN = "G", "Green", (0, 1, 0), "00ff00"

        # change meaning of default indirectly
        BLUE = "B", "Blue", (0, 0, 1), "000000"
        BLACK = "K", "Black", (0, 0, 0), "0000ff"

    int_enum = EnumField(IntEnum, null=True, default=None)

    # default value unchanged
    color = EnumField(Color, default="000000")
