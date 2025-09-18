from datetime import date, datetime, time, timedelta
from decimal import Decimal
import typing as t
from django.db.models import IntegerChoices as DjangoIntegerChoices
from django.db.models import TextChoices as DjangoTextChoices
from django.utils.translation import gettext as _
from enum_properties import EnumProperties, IntEnumProperties, Symmetric, s

from django_enum.choices import FlagChoices, FloatChoices, IntegerChoices, TextChoices
from tests.utils import try_convert


class DJIntEnum(DjangoIntegerChoices):
    ONE = 1, "One"
    TWO = 2, "Two"
    THREE = 3, "Three"


class DJTextEnum(DjangoTextChoices):
    A = "A", "Label A"
    B = "B", "Label B"
    C = "C", "Label C"


class TextEnum(TextChoices):
    version: int
    help: str
    aliases: t.Annotated[t.List[str], Symmetric(case_fold=True)]

    VALUE1 = (
        "V1",
        "Value1",
        0,
        _("Some help text about value1."),
        ["val1", "v1", "v one"],
    )
    VALUE2 = (
        "V22",
        "Value2",
        1,
        _("Some help text about value2."),
        {"val22", "v2", "v two"},
    )
    VALUE3 = (
        "V333",
        "Value3",
        2,
        _("Some help text about value3."),
        ["val333", "v3", "v three"],
    )
    DEFAULT = (
        "D",
        "Default",
        3,
        _("Some help text about default."),
        {"default", "defacto", "none"},
    )


class Constants(FloatChoices):
    symbol: t.Annotated[str, Symmetric()]

    PI = 3.14159265358979323846264338327950288, "Pi", "π"
    e = 2.71828, "Euler's Number", "e"
    GOLDEN_RATIO = 1.61803398874989484820458683436563811, "Golden Ratio", "φ"


class SmallPosIntEnum(IntegerChoices):
    VAL1 = 0, "Value 1"
    VAL2 = 2, "Value 2"
    VAL3 = 32767, "Value 32767"


class SmallIntEnum(IntegerChoices):
    VALn1 = -32768, "Value -32768"
    VAL0 = 0, "Value 0"
    VAL1 = 1, "Value 1"
    VAL2 = 2, "Value 2"
    VAL3 = 32767, "Value 32767"


class IntEnum(IntegerChoices):
    VALn1 = -2147483648, "Value -2147483648"
    VAL0 = 0, "Value 0"
    VAL1 = 1, "Value 1"
    VAL2 = 2, "Value 2"
    VAL3 = 2147483647, "Value 2147483647"


class PosIntEnum(IntegerChoices):
    VAL0 = 0, "Value 0"
    VAL1 = 1, "Value 1"
    VAL2 = 2, "Value 2"
    VAL3 = 2147483647, "Value 2147483647"


class BigPosIntEnum(IntegerChoices):
    VAL0 = 0, "Value 0"
    VAL1 = 1, "Value 1"
    VAL2 = 2, "Value 2"
    VAL3 = 2147483648, "Value 2147483648"


class BigIntEnum(IntegerChoices):
    pos: t.Annotated[BigPosIntEnum, Symmetric()]
    help: str

    VAL0 = (
        -2147483649,
        "Value -2147483649",
        BigPosIntEnum.VAL0,
        _("One less than the least regular integer."),
    )
    VAL1 = 1, "Value 1", BigPosIntEnum.VAL1, _("Something in the middle.")
    VAL2 = 2, "Value 2", BigPosIntEnum.VAL2, _("Something in the middle.")
    VAL3 = (
        2147483648,
        "Value 2147483648",
        BigPosIntEnum.VAL3,
        _("One more than the greatest regular integer."),
    )


class DateEnum(EnumProperties):
    label: t.Annotated[str, Symmetric()]

    BRIAN = date(1984, 8, 7), "Brian"
    EMMA = date(1989, 7, 27), "Emma"
    HUGO = date(2016, 9, 9), "Hugo"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls(try_convert(date, value, raise_on_error=True))
        return super()._missing_(value)

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                return self == DateEnum(other)
            except ValueError:
                return False
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class DateTimeEnum(EnumProperties):
    label: t.Annotated[str, Symmetric()]

    ST_HELENS = datetime(1980, 5, 18, 8, 32, 0), "Mount St. Helens"
    PINATUBO = datetime(1991, 6, 15, 20, 9, 0), "Pinatubo"
    KATRINA = datetime(2005, 8, 29, 5, 10, 0), "Katrina"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls(try_convert(datetime, value, raise_on_error=True))
        return super()._missing_(value)

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                return self == DateTimeEnum(other)
            except ValueError:
                return False
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class TimeEnum(EnumProperties):
    label: t.Annotated[str, Symmetric()]

    COB = time(17, 0, 0), "Close of Business"
    LUNCH = time(12, 30, 0), "Lunch"
    MORNING = time(9, 0, 0), "Morning"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls(try_convert(time, value, raise_on_error=True))
        return super()._missing_(value)

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                return self == TimeEnum(other)
            except ValueError:
                return False
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class DurationEnum(EnumProperties):
    label: t.Annotated[str, Symmetric(case_fold=True)]

    DAY = timedelta(days=1), "DAY"
    WEEK = timedelta(weeks=1), "WEEK"
    FORTNIGHT = timedelta(weeks=2), "FORTNIGHT"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls(try_convert(timedelta, value, raise_on_error=True))
        return super()._missing_(value)

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                return self == DurationEnum(other)
            except ValueError:
                return False
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class DecimalEnum(EnumProperties):
    label: t.Annotated[str, Symmetric(case_fold=True)]

    ONE = Decimal("0.99"), "One"
    TWO = Decimal("0.999"), "Two"
    THREE = Decimal("0.9999"), "Three"
    FOUR = Decimal("99.9999"), "Four"
    FIVE = Decimal("999"), "Five"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, (int, float, str)):
            return cls(try_convert(Decimal, value, raise_on_error=True))
        return super()._missing_(value)

    def __eq__(self, other):
        if isinstance(other, Decimal):
            return self.value == other
        if isinstance(other, str) and other or isinstance(other, (float, int)):
            try:
                return super().__eq__(DecimalEnum(str(other)))
            except ValueError:  # pragma: no cover
                return False
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class PrecedenceTest(IntegerChoices):
    prop1: t.Annotated[t.Union[int, str], Symmetric()]
    prop2: t.Annotated[float, Symmetric()]
    prop3: t.Annotated[str, Symmetric(case_fold=False)]
    prop4: t.Annotated[t.List[t.Union[str, float, int]], Symmetric(case_fold=True)]

    P1 = 0, "Precedence 1", 3, 0.1, _("First"), ["0.4", "Fourth", 1]
    P2 = 1, "Precedence 2", 2, 0.2, _("Second"), ["0.3", "Third", 2]
    P3 = 2, "Precedence 3", "1", 0.3, _("Third"), [0.2, "Second", 3]
    P4 = 3, "Precedence 4", 0, 0.4, _("Fourth"), [0.1, "First", 4]


class CarrierFrequency(FlagChoices):
    mhz: float

    L1 = 1, 1575.420
    L2 = 2, 1227.600
    L5 = 4, 1176.450

    G1 = 8, 1602.000
    G2 = 16, 1246.000

    E1 = 32, 1575.420
    E6 = 64, 1278.750
    E5 = 128, 1191.795
    E5a = 256, 1176.450
    E5b = 512, 1207.140

    B1 = 1024, 1561.100
    B2 = 2048, 1207.140
    B3 = 4096, 1268.520


class GNSSConstellation(FlagChoices):
    _symmetric_builtins_ = ["name", s("label", Symmetric(case_fold=True))]

    country: t.Annotated[str, Symmetric()]
    satellites: int
    frequencies: CarrierFrequency

    GPS = (
        1,
        "USA",
        31,
        CarrierFrequency.L1 | CarrierFrequency.L2 | CarrierFrequency.L5,
    )
    GLONASS = 2, "Russia", 24, CarrierFrequency.G1 | CarrierFrequency.G2
    GALILEO = (
        4,
        "EU",
        30,
        CarrierFrequency.E1
        | CarrierFrequency.E5
        | CarrierFrequency.E5a
        | CarrierFrequency.E5b
        | CarrierFrequency.E6,
    )
    BEIDOU = (
        8,
        "China",
        30,
        CarrierFrequency.B1 | CarrierFrequency.B2 | CarrierFrequency.B3,
    )
    QZSS = (
        16,
        "Japan",
        7,
        CarrierFrequency.L1 | CarrierFrequency.L2 | CarrierFrequency.L5,
    )


class LargeBitField(FlagChoices):
    ONE = 2**0, "One"
    TWO = 2**128, "Two"


class LargeNegativeField(IntegerChoices):
    NEG_ONE = -(2**128), "Negative One"
    ZERO = -1, "ZERO"


class ExternEnum(IntEnumProperties):
    """
    Tests that externally defined (i.e. not deriving from choices enums
    are supported.
    """

    label: t.Annotated[str, Symmetric(case_fold=True)]

    ONE = 1, "One"
    TWO = 2, "Two"
    THREE = 3, "Three"


class SmallPositiveFlagEnum(FlagChoices):
    number: t.Annotated[int, Symmetric()]

    ONE = 2**10, "One", 1
    TWO = 2**11, "Two", 2
    THREE = 2**12, "Three", 3
    FOUR = 2**13, "Four", 4
    FIVE = 2**14, "Five", 5


class PositiveFlagEnum(FlagChoices):
    number: t.Annotated[int, Symmetric()]

    ONE = 2**26, "One", 1
    TWO = 2**27, "Two", 2
    THREE = 2**28, "Three", 3
    FOUR = 2**29, "Four", 4
    FIVE = 2**30, "Five", 5


class BigPositiveFlagEnum(FlagChoices):
    version: t.Annotated[float, Symmetric()]

    ONE = 2**58, "One", 1.1
    TWO = 2**59, "Two", 2.2
    THREE = 2**60, "Three", 3.3
    FOUR = 2**61, "Four", 4.4
    FIVE = 2**62, "Five", 5.5


class ExtraBigPositiveFlagEnum(FlagChoices):
    version: t.Annotated[float, Symmetric()]

    ONE = 2**61, "One", 1.1
    TWO = 2**62, "Two", 2.2
    THREE = 2**63, "Three", 3.3
    FOUR = 2**64, "Four", 4.4
    FIVE = 2**65, "Five", 5.5


class SmallNegativeFlagEnum(FlagChoices):
    ONE = -(2**11), "One"
    TWO = -(2**12), "Two"
    THREE = -(2**13), "Three"
    FOUR = -(2**14), "Four"
    FIVE = -(2**15), "Five"


class NegativeFlagEnum(FlagChoices):
    ONE = -(2**27), "One"
    TWO = -(2**28), "Two"
    THREE = -(2**29), "Three"
    FOUR = -(2**30), "Four"
    FIVE = -(2**31), "Five"


class BigNegativeFlagEnum(FlagChoices):
    ONE = -(2**59), "One"
    TWO = -(2**60), "Two"
    THREE = -(2**61), "Three"
    FOUR = -(2**62), "Four"
    FIVE = -(2**63), "Five"


class ExtraBigNegativeFlagEnum(FlagChoices):
    ONE = -(2**62), "One"
    TWO = -(2**63), "Two"
    THREE = -(2**64), "Three"
    FOUR = -(2**65), "Four"
    FIVE = -(2**66), "Five"
