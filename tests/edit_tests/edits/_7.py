import typing as t
from typing_extensions import Annotated

from django.db import models
from enum_properties import Symmetric

from django_enum import EnumField
from django_enum.choices import TextChoices


class MigrationTester(models.Model):
    # remove enumeration

    # no change
    class Color(TextChoices):
        rgb: Annotated[t.Tuple[int, int, int], Symmetric()]
        hex: Annotated[str, Symmetric(case_fold=True)]

        # name   value   label       rgb       hex
        RD = "R", "Red", (1, 0, 0), "ff0000"
        GR = "G", "Green", (0, 1, 0), "00ff00"
        BL = "B", "Blue", (0, 0, 1), "0000ff"

    color = EnumField(Color)
