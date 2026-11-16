import sys

from django.db import models

from django_enum import EnumField

if sys.version_info >= (3, 11):
    from tests.flag_constraints.enums import (
        ConformFlagEnum,
        EjectFlagEnum,
        KeepFlagEnum,
        StrictBigTopBitFlagEnum,
        StrictFlagEnum,
        StrictTopBitFlagEnum,
    )

    class FlagConstraintTestModel(models.Model):
        keep = EnumField(KeepFlagEnum, null=True, default=None, blank=True)
        eject = EnumField(
            EjectFlagEnum, null=False, default=EjectFlagEnum(0), blank=True
        )
        eject_non_strict = EnumField(
            EjectFlagEnum,
            null=False,
            default=EjectFlagEnum(0),
            blank=True,
            strict=False,
        )
        conform = EnumField(ConformFlagEnum, null=True, default=None, blank=True)
        strict = EnumField(StrictFlagEnum, null=True, default=None, blank=True)
        strict_top = EnumField(
            StrictTopBitFlagEnum, null=True, default=None, blank=True
        )
        strict_big_top = EnumField(
            StrictBigTopBitFlagEnum, null=False, default=StrictBigTopBitFlagEnum(0)
        )
