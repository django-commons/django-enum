import enum
from enum import IntFlag

from django.db import models
from django.db.models import TextChoices
from django.urls import reverse

from django_enum import EnumField
from tests.djenum.enums import (
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
    IntEnum,
    MultiPrimitiveEnum,
    MultiWithNone,
    NegativeFlagEnum,
    NullableExternEnum,
    NullableStrEnum,
    PathEnum,
    PosIntEnum,
    PositiveFlagEnum,
    SmallIntEnum,
    SmallNegativeFlagEnum,
    SmallPosIntEnum,
    SmallPositiveFlagEnum,
    StrProps,
    StrPropsEnum,
    StrTestEnum,
    TextEnum,
    TimeEnum,
    NullableConstants,
    GNSSConstellation,
    NestStatusBasic,
    NestStatusInt,
    NestStatusBasicInt,
    NestStatusStr,
)


class EnumTester(models.Model):
    small_pos_int = EnumField(
        SmallPosIntEnum, null=True, default=None, db_index=True, blank=True
    )
    small_int = EnumField(
        SmallIntEnum, null=False, default=SmallIntEnum.VAL3, db_index=True, blank=True
    )

    pos_int = EnumField(PosIntEnum, default=2147483647, db_index=True, blank=True)
    int = EnumField(IntEnum, null=True, db_index=True, blank=True)

    big_pos_int = EnumField(
        BigPosIntEnum, null=True, default=None, db_index=True, blank=True
    )
    big_int = EnumField(BigIntEnum, default=-2147483649, db_index=True, blank=True)

    constant = EnumField(Constants, null=True, default=None, db_index=True, blank=True)

    text = EnumField(TextEnum, null=True, default=None, db_index=True, blank=True)

    extern = EnumField(ExternEnum, null=True, default=None, db_index=True, blank=True)

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

    dj_int_enum = EnumField(DJIntEnum, default=DJIntEnum.ONE)
    dj_text_enum = EnumField(DJTextEnum, default="A")

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

    # eccentric enums
    date_enum = EnumField(
        DateEnum,
        null=False,
        default=DateEnum.EMMA,
        blank=True,
        choices=[
            (DateEnum.EMMA, "Emma"),
            (DateEnum.BRIAN, "Brian"),
            (DateEnum.HUGO, "Hugo"),
        ],
    )
    datetime_enum = EnumField(
        DateTimeEnum, null=True, default=None, blank=True, strict=False
    )
    time_enum = EnumField(TimeEnum, null=True, default=None, blank=True)

    duration_enum = EnumField(DurationEnum, null=True, default=None, blank=True)

    decimal_enum = EnumField(
        DecimalEnum,
        null=False,
        default=DecimalEnum.THREE.value,
        blank=True,
        choices=[
            (DecimalEnum.ONE.value, "One"),
            (DecimalEnum.TWO.value, "Two"),
            (DecimalEnum.THREE.value, "Three"),
            (DecimalEnum.FOUR.value, "Four"),
            (DecimalEnum.FIVE.value, "Five"),
        ],
    )

    def get_absolute_url(self):
        return reverse("tests_djenum:enum-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class BadDefault(models.Model):
    # Non-strict
    non_strict_int = EnumField(SmallPosIntEnum, null=True, default=5, blank=True)


class AdminDisplayBug35(models.Model):
    text_enum = EnumField(TextEnum, default=TextEnum.VALUE1)

    int_enum = EnumField(SmallPosIntEnum, default=SmallPosIntEnum.VAL2)

    blank_int = EnumField(SmallPosIntEnum, null=True, default=None)

    blank_txt = EnumField(TextEnum, null=True, default=None)

    status_basic = EnumField(NestStatusBasic, null=True, default=None)
    status_basic_int = EnumField(NestStatusBasicInt, null=True, default=None)
    status_int = EnumField(NestStatusInt, null=True, default=None)
    status_str = EnumField(NestStatusStr, null=True, default=None)


class EmptyEnumValueTester(models.Model):
    class BlankTextEnum(TextChoices):
        VALUE1 = "", "Value1"
        VALUE2 = "V22", "Value2"

    class NoneIntEnum(enum.Enum):
        VALUE1 = None
        VALUE2 = 2

    blank_text_enum = EnumField(BlankTextEnum, default="")
    none_int_enum = EnumField(NoneIntEnum, null=True, default=None)

    # should not be possible to store NoneIntEnum.VALUE1
    none_int_enum_non_null = EnumField(NoneIntEnum, null=False)


class EnumFlagTesterBase(models.Model):
    small_pos = EnumField(
        SmallPositiveFlagEnum, default=None, null=True, db_index=True, blank=True
    )

    pos = EnumField(
        PositiveFlagEnum, default=PositiveFlagEnum(0), db_index=True, blank=True
    )

    big_pos = EnumField(
        BigPositiveFlagEnum, default=BigPositiveFlagEnum(0), db_index=True, blank=True
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
        BigNegativeFlagEnum, default=BigNegativeFlagEnum(0), db_index=True, blank=True
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


class EnumFlagTester(EnumFlagTesterBase):
    small_pos = EnumField(
        SmallPositiveFlagEnum, default=None, null=True, db_index=True, blank=True
    )

    pos = EnumField(
        PositiveFlagEnum, default=PositiveFlagEnum(0), db_index=True, blank=True
    )

    big_pos = EnumField(
        BigPositiveFlagEnum, default=BigPositiveFlagEnum(0), db_index=True, blank=True
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
        BigNegativeFlagEnum, default=BigNegativeFlagEnum(0), db_index=True, blank=True
    )

    extra_big_neg = EnumField(
        ExtraBigNegativeFlagEnum,
        default=None,
        db_index=True,
        blank=True,
        null=True,
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


class EnumFlagTesterRelated(EnumFlagTesterBase):
    related_flags = models.ManyToManyField(EnumFlagTester, related_name="related_flags")


class MultiPrimitiveTestModel(models.Model):
    # primitive will default to string
    multi = EnumField(MultiPrimitiveEnum, null=True, default=None, blank=True)

    # primitive will be a float
    multi_float = EnumField(
        MultiPrimitiveEnum, primitive=float, null=True, default="2.0", blank=True
    )

    multi_none = EnumField(MultiWithNone, default=MultiWithNone.VAL1, blank=True)

    multi_none_unconstrained = EnumField(
        MultiWithNone, default=MultiWithNone.VAL1, blank=True, constrained=False
    )

    multi_unconstrained_non_strict = EnumField(
        MultiPrimitiveEnum,
        default=MultiPrimitiveEnum.VAL1,
        blank=True,
        constrained=False,
        strict=False,
    )


class CustomPrimitiveTestModel(models.Model):
    path = EnumField(PathEnum, primitive=str)

    str_props = EnumField(StrPropsEnum, primitive=str)


class TestNullableFloat(models.Model):
    nullable_float = EnumField(NullableConstants, default=None, blank=True, null=True)


class NameOverrideTest(models.Model):
    class TextEnum(models.TextChoices):
        VALUE0 = "V0", "Value 0"
        VALUE1 = "V1", "Value 1"
        VALUE2 = "V2", "Value 2"

    txt_enum = EnumField(
        TextEnum, name="enum_field", null=True, blank=True, default=None
    )


class NullBlankFormTester(models.Model):
    required = EnumField(ExternEnum)
    required_default = EnumField(ExternEnum, default=ExternEnum.TWO)
    # this is allowed but will result in validation errors on form submission with null selected
    blank = EnumField(ExternEnum, null=False, blank=True)
    # this is allowed but you will not be able to submit nulls via a form
    # this is beyond the scope of django-enum - implement custom form logic to do this
    # nullable = EnumField(ExternEnum, null=True)
    blank_nullable = EnumField(ExternEnum, null=True, blank=True)
    blank_nullable_default = EnumField(ExternEnum, null=True, blank=True, default=None)


class NullableBlankFormTester(models.Model):
    required = EnumField(NullableExternEnum)
    required_default = EnumField(NullableExternEnum, default=NullableExternEnum.TWO)
    # this is allowed but will result in validation errors on form submission with null selected
    blank = EnumField(NullableExternEnum, null=False, blank=True)
    # this is allowed but you will not be able to submit nulls via a form
    # this is beyond the scope of django-enum - implement custom form logic to do this
    # nullable = EnumField(ExternEnum, null=True)
    blank_nullable = EnumField(NullableExternEnum, null=True, blank=True)
    blank_nullable_default = EnumField(
        NullableExternEnum, null=True, blank=True, default=None
    )


class NullableStrFormTester(models.Model):
    required = EnumField(NullableStrEnum)
    required_default = EnumField(NullableStrEnum, default=NullableStrEnum.STR2)
    # this is allowed but will result in validation errors on form submission with null selected
    blank = EnumField(NullableStrEnum, null=False, blank=True)
    # this is allowed but you will not be able to submit nulls via a form
    # this is beyond the scope of django-enum - implement custom form logic to do this
    # nullable = EnumField(ExternEnum, null=True)
    blank_nullable = EnumField(NullableStrEnum, null=True, blank=True)
    blank_nullable_default = EnumField(
        NullableStrEnum, null=True, blank=True, default=NullableStrEnum.NONE
    )


class Bug53Tester(models.Model):
    char_blank_null_true = EnumField(StrTestEnum, null=True, blank=True)
    char_blank_null_false = EnumField(StrTestEnum, null=False, blank=True)
    char_blank_null_false_default = EnumField(
        StrTestEnum, null=False, blank=True, default="", strict=False
    )
    int_blank_null_false = EnumField(ExternEnum, null=False, blank=True)
    int_blank_null_true = EnumField(ExternEnum, null=True, blank=True)


class AltWidgetTester(models.Model):
    text = EnumField(TextEnum, default=TextEnum.VALUE1)
    text_null = EnumField(TextEnum, default=None, blank=True, null=True)
    text_non_strict = EnumField(
        TextEnum, default=TextEnum.VALUE1, strict=False, max_length=10
    )
    constellation = EnumField(GNSSConstellation)
    constellation_null = EnumField(
        GNSSConstellation, null=True, blank=True, default=None
    )
    constellation_non_strict = EnumField(GNSSConstellation, strict=False)


class FlagFilterTester(models.Model):
    small_flag = EnumField(enum=SmallPositiveFlagEnum, null=True, default=None)
    flag = EnumField(enum=PositiveFlagEnum)
    flag_no_coerce = EnumField(enum=PositiveFlagEnum, coerce=False)
    big_flag = EnumField(enum=BigPositiveFlagEnum, strict=False)
    # extra_big_flag = EnumField(enum=ExtraBigPositiveFlagEnum)

    def get_absolute_url(self):
        return reverse("tests_djenum:flag-detail", kwargs={"pk": self.pk})
