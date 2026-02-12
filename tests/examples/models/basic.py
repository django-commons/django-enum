# flake8: noqa
from django.db import models
from django_enum import EnumField
from django_enum.fields import EnumCharField
from django.db.models import Field


class BasicExample(models.Model):

    class TextEnum(models.TextChoices):

        VALUE0 = "V0", "Value 0"
        VALUE1 = "V1", "Value 1"
        VALUE2 = "V2", "Value 2"

    class IntEnum(models.IntegerChoices):

        # fmt: off
        ONE   = 1, "One"
        TWO   = 2, "Two"
        THREE = 3, "Three"
        # fmt: on

    # this is equivalent to:
    #  CharField(max_length=2, choices=TextEnum.choices, null=True, blank=True)
    txt_enum: EnumCharField[TextEnum] = EnumCharField(TextEnum, str, null=True, blank=True, default=None)

    # this is equivalent to
    #  PositiveSmallIntegerField(choices=IntEnum.choices, default=IntEnum.ONE.value)
    int_enum = EnumField(IntEnum, default=IntEnum.ONE)
