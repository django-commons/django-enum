# flake8: noqa
import typing as t
from django.db import models
from django_enum import EnumField
from django_enum.choices import TextChoices
from enum_properties import Symmetric, symmetric


class TextChoicesExample(models.Model):

    class Color(TextChoices):

        # no need to specify label because it is built in
        rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
        hex: t.Annotated[str, Symmetric(case_fold=True)]

        # fmt: off
        # name value label       rgb       hex
        RED   = "R", "Red",   (1, 0, 0), "ff0000"
        GREEN = "G", "Green", (0, 1, 0), "00ff00"
        BLUE  = "B", "Blue",  (0, 0, 1), "0000ff"
        # fmt: on

        # by default label is symmetric, but case sensitive
        # to make it case-insensitive we can override the property
        # and mark it like this:
        @symmetric(case_fold=True)  # type: ignore[prop-decorator]
        @property
        def label(self) -> str:
            return str(self._label_)

    color = EnumField(Color)
