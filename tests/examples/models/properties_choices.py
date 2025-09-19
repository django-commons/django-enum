# flake8: noqa
import typing as t
from django.db import models
from enum_properties import Symmetric
from django_enum import EnumField
from django_enum.choices import TextChoices

class ChoicesWithProperties(models.Model):

    class Color(TextChoices):

        # label is added as a symmetric property by the base class
        rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
        hex: t.Annotated[str, Symmetric(case_fold=True)]

        # fmt: off
        # name value label       rgb       hex
        RED   = "R", "Red",   (1, 0, 0), "ff0000"
        GREEN = "G", "Green", (0, 1, 0), "00ff00"
        BLUE  = "B", "Blue",  (0, 0, 1), "0000ff"
        # fmt: on

    color = EnumField(Color)
