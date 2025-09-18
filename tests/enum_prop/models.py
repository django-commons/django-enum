from django.db import models
from django.urls import reverse
from enum_properties import StrEnumProperties, IntEnumProperties, Symmetric
import typing as t

from django_enum import EnumField
from tests.enum_prop.enums import (
    BigIntEnum,
    BigNegativeFlagEnum,
    BigPosIntEnum,
    BigPositiveFlagEnum,
    Constants,
    DateEnum,
    DateTimeEnum,
    DecimalEnum,
    DJIntEnum,
    DJTextEnum,
    DurationEnum,
    ExternEnum,
    ExtraBigNegativeFlagEnum,
    ExtraBigPositiveFlagEnum,
    GNSSConstellation,
    IntEnum,
    LargeBitField,
    LargeNegativeField,
    NegativeFlagEnum,
    PosIntEnum,
    PositiveFlagEnum,
    SmallIntEnum,
    SmallNegativeFlagEnum,
    SmallPosIntEnum,
    SmallPositiveFlagEnum,
    TextEnum,
    TimeEnum,
)


class EnumTester(models.Model):
    small_pos_int = EnumField(
        SmallPosIntEnum, null=True, default=None, db_index=True, blank=True
    )
    small_int = EnumField(
        SmallIntEnum, null=False, default="Value 32767", db_index=True, blank=True
    )

    pos_int = EnumField(PosIntEnum, default=2147483647, db_index=True, blank=True)
    int = EnumField(IntEnum, null=True, db_index=True, blank=True)

    big_pos_int = EnumField(
        BigPosIntEnum, null=True, default=None, db_index=True, blank=True
    )
    big_int = EnumField(
        BigIntEnum, default=BigPosIntEnum.VAL0, db_index=True, blank=True
    )

    constant = EnumField(Constants, null=True, default=None, db_index=True, blank=True)

    text = EnumField(TextEnum, null=True, default=None, db_index=True, blank=True)

    # eccentric enums
    date_enum = EnumField(DateEnum, null=False, default=DateEnum.EMMA, blank=True)

    datetime_enum = EnumField(
        DateTimeEnum, null=True, default=None, blank=True, strict=False
    )

    time_enum = EnumField(TimeEnum, null=True, default=None, blank=True)

    duration_enum = EnumField(DurationEnum, null=True, default=None, blank=True)

    decimal_enum = EnumField(
        DecimalEnum, null=False, default=DecimalEnum.THREE.value, blank=True
    )

    extern = EnumField(ExternEnum, null=True, default=None, db_index=True, blank=True)

    # basic choice fields - used to compare behavior
    int_choice = models.IntegerField(
        default=1,
        null=False,
        blank=True,
        choices=((1, "One"), (2, "Two"), (3, "Three")),
    )

    char_choice = models.CharField(
        max_length=50,
        default="A",
        null=False,
        blank=True,
        choices=(("A", "First"), ("B", "Second"), ("C", "Third")),
    )

    int_field = models.IntegerField(default=1, null=False, blank=True)

    float_field = models.FloatField(default=1.5, null=False, blank=True)

    char_field = models.CharField(max_length=1, default="A", null=False, blank=True)
    ################################################

    dj_int_enum = EnumField(DJIntEnum, default=DJIntEnum.ONE)
    dj_text_enum = EnumField(DJTextEnum, default=DJTextEnum.A)

    # Non-strict
    non_strict_int = EnumField(
        SmallPosIntEnum, strict=False, null=True, default=5, blank=True
    )
    non_strict_text = EnumField(
        TextEnum, max_length=12, strict=False, null=False, default="", blank=True
    )

    no_coerce = EnumField(
        SmallPosIntEnum, coerce=False, null=True, default=None, blank=True
    )

    # flags
    gnss = EnumField(
        GNSSConstellation,
        null=False,
        default=(GNSSConstellation.GPS | GNSSConstellation.GLONASS),
        blank=True,
    )

    def get_absolute_url(self):
        return reverse("tests_enum_prop:enum-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)
        # constraints = []


class MyModel(models.Model):
    class TextEnum(StrEnumProperties):
        label: str

        VALUE0 = "V0", "Value 0"
        VALUE1 = "V1", "Value 1"
        VALUE2 = "V2", "Value 2"

    class IntEnum(IntEnumProperties):
        label: str

        ONE = 1, "One"
        TWO = (
            2,
            "Two",
        )
        THREE = 3, "Three"

    class Color(StrEnumProperties):
        label: t.Annotated[str, Symmetric()]
        rgb: t.Annotated[t.Tuple[int, int, int], Symmetric()]
        hex: t.Annotated[str, Symmetric(case_fold=True)]

        # name   value   label       rgb       hex
        RED = "R", "Red", (1, 0, 0), "ff0000"
        GREEN = "G", "Green", (0, 1, 0), "00ff00"
        BLUE = "B", "Blue", (0, 0, 1), "0000ff"

    txt_enum = EnumField(TextEnum, null=True, blank=True)
    int_enum = EnumField(IntEnum)
    color = EnumField(Color)


class AdminDisplayBug35(models.Model):
    text_enum = EnumField(TextEnum, default=TextEnum.VALUE1)

    int_enum = EnumField(SmallPosIntEnum, default=SmallPosIntEnum.VAL2)

    blank_int = EnumField(SmallPosIntEnum, null=True, default=None)

    blank_txt = EnumField(TextEnum, null=True, default=None)


class PerfCompare(models.Model):
    small_pos_int = models.PositiveSmallIntegerField(
        choices=SmallPosIntEnum.choices,
        null=True,
        default=None,
        db_index=True,
        blank=True,
    )
    small_int = models.SmallIntegerField(
        choices=SmallIntEnum.choices,
        null=False,
        default=SmallIntEnum.VAL3,
        db_index=True,
        blank=True,
    )
    pos_int = models.PositiveIntegerField(
        choices=PosIntEnum.choices,
        default=PosIntEnum.VAL3,
        db_index=True,
        blank=True,
    )
    int = models.IntegerField(
        choices=IntEnum.choices, null=True, db_index=True, blank=True
    )
    big_pos_int = models.PositiveBigIntegerField(
        choices=BigPosIntEnum.choices,
        null=True,
        default=None,
        db_index=True,
        blank=True,
    )
    big_int = models.BigIntegerField(
        choices=BigIntEnum.choices,
        default=BigIntEnum.VAL0,
        db_index=True,
        blank=True,
    )
    constant = models.FloatField(
        choices=Constants.choices,
        null=True,
        default=None,
        db_index=True,
        blank=True,
    )
    text = models.CharField(
        choices=TextEnum.choices,
        max_length=4,
        null=True,
        default=None,
        db_index=True,
        blank=True,
    )

    # basic choice fields - used to compare behavior
    int_choice = models.IntegerField(
        default=1,
        null=False,
        blank=True,
        choices=((1, "One"), (2, "Two"), (3, "Three")),
    )
    char_choice = models.CharField(
        max_length=1,
        default="A",
        null=False,
        blank=True,
        choices=(("A", "First"), ("B", "Second"), ("C", "Third")),
    )
    int_field = models.IntegerField(default=1, null=False, blank=True)
    float_field = models.FloatField(default=1.5, null=False, blank=True)
    char_field = models.CharField(max_length=1, default="A", null=False, blank=True)
    ################################################

    dj_int_enum = models.PositiveSmallIntegerField(
        choices=DJIntEnum.choices, default=DJIntEnum.ONE.value
    )
    dj_text_enum = models.CharField(
        choices=DJTextEnum.choices, default=DJTextEnum.A.value, max_length=1
    )

    # Non-strict
    non_strict_int = models.PositiveSmallIntegerField(
        choices=SmallPosIntEnum.choices, null=True, default=None, blank=True
    )
    non_strict_text = EnumField(
        TextEnum, max_length=12, strict=False, null=False, default="", blank=True
    )
    no_coerce = EnumField(
        SmallPosIntEnum, coerce=False, null=True, default=None, blank=True
    )

    class Meta:
        ordering = ("id",)


class NoCoercePerfCompare(models.Model):
    small_pos_int = EnumField(
        SmallPosIntEnum,
        coerce=False,
        null=True,
        default=None,
        db_index=True,
        blank=True,
    )
    small_int = EnumField(
        SmallIntEnum,
        coerce=False,
        null=False,
        default=SmallIntEnum.VAL3,
        db_index=True,
        blank=True,
    )
    pos_int = EnumField(
        PosIntEnum, coerce=False, default=PosIntEnum.VAL3, db_index=True, blank=True
    )
    int = EnumField(IntEnum, coerce=False, null=True, db_index=True, blank=True)
    big_pos_int = EnumField(
        BigPosIntEnum,
        coerce=False,
        null=True,
        default=None,
        db_index=True,
        blank=True,
    )
    big_int = EnumField(
        BigIntEnum, coerce=False, default=BigIntEnum.VAL0, db_index=True, blank=True
    )
    constant = EnumField(
        Constants, coerce=False, null=True, default=None, db_index=True, blank=True
    )
    text = EnumField(
        TextEnum, coerce=False, null=True, default=None, db_index=True, blank=True
    )

    # basic choice fields - used to compare behavior
    int_choice = models.IntegerField(
        default=1,
        null=False,
        blank=True,
        choices=((1, "One"), (2, "Two"), (3, "Three")),
    )
    char_choice = models.CharField(
        max_length=1,
        default="A",
        null=False,
        blank=True,
        choices=(("A", "First"), ("B", "Second"), ("C", "Third")),
    )
    int_field = models.IntegerField(default=1, null=False, blank=True)
    float_field = models.FloatField(default=1.5, null=False, blank=True)
    char_field = models.CharField(max_length=1, default="A", null=False, blank=True)
    ################################################

    dj_int_enum = EnumField(DJIntEnum, coerce=False, default=DJIntEnum.ONE)
    dj_text_enum = EnumField(DJTextEnum, coerce=False, default=DJTextEnum.A)

    # Non-strict
    non_strict_int = EnumField(
        SmallPosIntEnum,
        coerce=False,
        strict=False,
        null=True,
        default=None,
        blank=True,
    )
    non_strict_text = EnumField(
        TextEnum,
        coerce=False,
        max_length=12,
        strict=False,
        null=False,
        default="",
        blank=True,
    )
    no_coerce = EnumField(
        SmallPosIntEnum, coerce=False, null=True, default=None, blank=True
    )

    class Meta:
        ordering = ("id",)


class SingleEnumPerf(models.Model):
    small_pos_int = EnumField(
        enum=SmallPosIntEnum, null=True, default=None, db_index=True, blank=True
    )


class SingleFieldPerf(models.Model):
    small_pos_int = models.PositiveSmallIntegerField(
        choices=SmallPosIntEnum.choices,
        null=True,
        default=None,
        db_index=True,
        blank=True,
    )


class SingleNoCoercePerf(models.Model):
    small_pos_int = EnumField(
        enum=SmallPosIntEnum,
        coerce=False,
        null=True,
        default=None,
        db_index=True,
        blank=True,
    )


class BitFieldModel(models.Model):
    bit_field_small = EnumField(GNSSConstellation)
    bit_field_large = EnumField(LargeBitField, null=True, default=None, blank=True)
    bit_field_large_empty_default = EnumField(LargeBitField, blank=True)
    large_neg = EnumField(
        LargeNegativeField, default=LargeNegativeField.NEG_ONE, null=True, blank=True
    )
    no_default = EnumField(LargeBitField)


class BaseEnumFlagPropTester(models.Model):
    small_pos = EnumField(
        SmallPositiveFlagEnum, default=None, null=True, db_index=True, blank=True
    )

    pos = EnumField(
        PositiveFlagEnum, default=PositiveFlagEnum(0), db_index=True, blank=True
    )

    big_pos = EnumField(
        BigPositiveFlagEnum,
        default=BigPositiveFlagEnum(0),
        db_index=True,
        blank=True,
    )

    extra_big_pos = EnumField(
        ExtraBigPositiveFlagEnum,
        default=ExtraBigPositiveFlagEnum(0),
        db_index=True,
        blank=True,
    )

    small_neg = EnumField(
        SmallNegativeFlagEnum,
        default=SmallNegativeFlagEnum(0),
        db_index=True,
        blank=True,
    )

    neg = EnumField(
        NegativeFlagEnum, default=NegativeFlagEnum(0), db_index=True, blank=True
    )

    big_neg = EnumField(
        BigNegativeFlagEnum,
        default=BigNegativeFlagEnum(0),
        db_index=True,
        blank=True,
    )

    extra_big_neg = EnumField(
        ExtraBigNegativeFlagEnum, default=None, db_index=True, blank=True, null=True
    )

    def __repr__(self):
        return (
            f"EnumFlagTester(small_pos={repr(self.small_pos)}, "
            f"pos={repr(self.pos)}, "
            f"big_pos={repr(self.big_pos)}, "
            f"extra_big_pos={repr(self.extra_big_pos)}, "
            f"small_neg={repr(self.small_neg)}, neg={repr(self.neg)}, "
            f"big_neg={repr(self.big_neg)}, "
            f"extra_big_neg={repr(self.extra_big_neg)})"
        )

    class Meta:
        abstract = True


class EnumFlagPropTester(BaseEnumFlagPropTester):
    pass


class EnumFlagPropTesterRelated(BaseEnumFlagPropTester):
    related_flags = models.ManyToManyField(
        EnumFlagPropTester, related_name="related_flags"
    )


class FlagFilterTester(models.Model):
    small_flag = EnumField(enum=SmallPositiveFlagEnum, null=True, default=None)
    flag = EnumField(enum=PositiveFlagEnum)
    flag_no_coerce = EnumField(enum=PositiveFlagEnum, coerce=False)
    big_flag = EnumField(enum=BigPositiveFlagEnum, strict=False)
    # extra_big_flag = EnumField(enum=ExtraBigPositiveFlagEnum)

    def get_absolute_url(self):
        return reverse("tests_enum_prop:flag-detail", kwargs={"pk": self.pk})
