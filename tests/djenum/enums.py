from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum, IntEnum, IntFlag
from pathlib import PurePosixPath

from django.db.models import IntegerChoices, TextChoices
from django.db.models.enums import Choices

from tests.utils import try_convert


class FloatChoices(float, Choices):
    def __str__(self):
        return str(self.value)


class DJIntEnum(IntegerChoices):
    ONE = 1, "One"
    TWO = 2, "Two"
    THREE = 3, "Three"


class DJTextEnum(TextChoices):
    A = "A", "Label A"
    B = "B", "Label B"
    C = "C", "Label C"


class TextEnum(TextChoices):
    VALUE1 = "V1", "Value1"
    VALUE2 = "V22", "Value2"
    VALUE3 = "V333", "Value3"
    DEFAULT = "D", "Default"


class ExternEnum(IntEnum):
    """
    Tests that externally defined (i.e. not deriving from choices enums
    are supported.
    """

    ONE = 1
    TWO = 2
    THREE = 3

    def __str__(self):
        return self.name


class NullableExternEnum(Enum):
    """
    Tests that externally defined (i.e. not deriving from choices enums
    are supported.
    """

    NONE = None
    ONE = 1
    TWO = 2
    THREE = 3

    def __str__(self):
        return self.name


class NullableStrEnum(Enum):
    NONE = None
    STR1 = "str1"
    STR2 = "str2"

    def __str__(self):
        return self.name


class Constants(FloatChoices):
    PI = 3.14159265358979323846264338327950288, "Pi"
    e = 2.71828, "Euler's Number"
    GOLDEN_RATIO = 1.61803398874989484820458683436563811, "Golden Ratio"


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
    VAL0 = -2147483649, "Value -2147483649"
    VAL1 = 1, "Value 1"
    VAL2 = 2, "Value 2"
    VAL3 = 2147483648, "Value 2147483648"


class DateEnum(Enum):
    BRIAN = date(1984, 8, 7)
    EMMA = date(1989, 7, 27)
    HUGO = date(2016, 9, 9)

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls(try_convert(date, value, raise_on_error=True))
        return super()._missing_(value)

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                return super().__eq__(DateEnum(other))
            except ValueError:
                return False
        if isinstance(other, date):
            return self.value == other
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class DateTimeEnum(Enum):
    ST_HELENS = datetime(1980, 5, 18, 8, 32, 0)
    PINATUBO = datetime(1991, 6, 15, 20, 9, 0)
    KATRINA = datetime(2005, 8, 29, 5, 10, 0)

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls(try_convert(datetime, value, raise_on_error=True))
        return super()._missing_(value)

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                return super().__eq__(DateTimeEnum(other))
            except ValueError:  # pragma: no cover
                return False
        if isinstance(other, datetime):
            return self.value == other
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class TimeEnum(Enum):
    COB = time(17, 0, 0)
    LUNCH = time(12, 30, 0)
    MORNING = time(9, 0, 0)

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls(try_convert(time, value, raise_on_error=True))
        return super()._missing_(value)

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                return super().__eq__(TimeEnum(other))
            except ValueError:
                return False
        if isinstance(other, time):
            return self.value == other
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class DurationEnum(Enum):
    DAY = timedelta(days=1)
    WEEK = timedelta(weeks=1)
    FORTNIGHT = timedelta(weeks=2)

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            return cls(try_convert(timedelta, value, raise_on_error=True))
        return super()._missing_(value)

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                return super().__eq__(DurationEnum(other))
            except ValueError:
                return False
        if isinstance(other, timedelta):
            return self.value == other
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class DecimalEnum(Enum):
    ONE = Decimal("0.99")
    TWO = Decimal("0.999")
    THREE = Decimal("0.9999")
    FOUR = Decimal("99.9999")
    FIVE = Decimal("999")

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


class NullableConstants(Enum):
    NONE = None
    PI = 3.14159265358979323846264338327950288
    e = 2.71828
    GOLDEN_RATIO = 1.61803398874989484820458683436563811


class SmallPositiveFlagEnum(IntFlag):
    ONE = 2**10
    TWO = 2**11
    THREE = 2**12
    FOUR = 2**13
    FIVE = 2**14


class PositiveFlagEnum(IntFlag):
    ONE = 2**26
    TWO = 2**27
    THREE = 2**28
    FOUR = 2**29
    FIVE = 2**30


class BigPositiveFlagEnum(IntFlag):
    ONE = 2**58
    TWO = 2**59
    THREE = 2**60
    FOUR = 2**61
    FIVE = 2**62


class ExtraBigPositiveFlagEnum(IntFlag):
    ONE = 2**0
    TWO = 2**1
    THREE = 2**63
    FOUR = 2**64
    FIVE = 2**65


# its possible to make negative valued flag enums, but the bitwise operations
# do not really work. We test them because they may be seen in the wild. At
# the DB level they behave like normal enumerations with a flag enumeration's
# check constraint by range instead of by value


class SmallNegativeFlagEnum(IntFlag):
    ONE = -(2**11)
    TWO = -(2**12)
    THREE = -(2**13)
    FOUR = -(2**14)
    FIVE = -(2**15)


class NegativeFlagEnum(IntFlag):
    ONE = -(2**27)
    TWO = -(2**28)
    THREE = -(2**29)
    FOUR = -(2**30)
    FIVE = -(2**31)


class BigNegativeFlagEnum(IntFlag):
    ONE = -(2**59)
    TWO = -(2**60)
    THREE = -(2**61)
    FOUR = -(2**62)
    FIVE = -(2**63)


class ExtraBigNegativeFlagEnum(IntFlag):
    ONE = -(2**0)
    TWO = -(2**1)
    THREE = -(2**64)
    FOUR = -(2**65)
    FIVE = -(2**66)


class MultiPrimitiveEnum(Enum):
    VAL1 = 1
    VAL2 = "2.0"
    VAL3 = 3.0
    VAL4 = Decimal("4.5")


class MultiWithNone(Enum):
    NONE = None
    VAL1 = 1
    VAL2 = "2.0"
    VAL3 = 3.0
    VAL4 = Decimal("4.5")


class PathEnum(Enum):
    USR = PurePosixPath("/usr")
    USR_LOCAL = PurePosixPath("/usr/local")
    USR_LOCAL_BIN = PurePosixPath("/usr/local/bin")


class StrProps:
    """
    Wrap a string with some properties.
    """

    _str = ""

    def __init__(self, string):
        self._str = string

    def __str__(self):
        return self._str

    @property
    def upper(self):
        return self._str.upper()

    @property
    def lower(self):
        return self._str.lower()

    def __eq__(self, other):
        if isinstance(other, str):
            return self._str == other
        if other is not None:
            return self._str == other._str
        return False

    def deconstruct(self):
        return "tests.djenum.enums.StrProps", (self._str,), {}


class StrPropsEnum(Enum):
    STR1 = StrProps("str1")
    STR2 = StrProps("str2")
    STR3 = StrProps("str3")


class StrTestEnum(str, Enum):
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"

    def __str__(self):
        return self.value


class GNSSConstellation(IntFlag):
    GPS = 1 << 0
    GLONASS = 1 << 1
    GALILEO = 1 << 2
    BEIDOU = 1 << 3
    QZSS = 1 << 4


class NestStatusBasic(Enum):
    INIT = "INIT"
    LOADED = "LOADED"
    ACTIVE = "ACTIVE"
    DONE = "DONE"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, value) -> bool:
        if isinstance(value, self.__class__):
            return self.value == value.value
        try:
            return self.value == self.__class__(value).value
        except (ValueError, TypeError):
            return False


class NestStatusStr(str, Enum):
    INIT = "INIT"
    LOADED = "LOADED"
    ACTIVE = "ACTIVE"
    DONE = "DONE"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


class NestStatusBasicInt(Enum):
    INIT = 0
    LOADED = 1
    ACTIVE = 2
    DONE = 3
    REJECTED = 4
    CANCELLED = 5

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, value) -> bool:
        if isinstance(value, self.__class__):
            return self.value == value.value
        try:
            return self.value == self.__class__(value).value
        except (ValueError, TypeError):
            return False


class NestStatusInt(int, Enum):
    INIT = 0
    LOADED = 1
    ACTIVE = 2
    DONE = 3
    REJECTED = 4
    CANCELLED = 5
