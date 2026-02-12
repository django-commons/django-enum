import re
import os
from datetime import date, datetime, time, timedelta
from decimal import Decimal, DecimalException
from pathlib import Path
from importlib.util import find_spec

from tests.oracle_patch import patch_oracle

duration_rgx1 = re.compile(
    r"(-)?(\d+) (?:days?, )?(\d{1,2}):(\d{2}):(\d{2})(?:\.(\d+))?", re.IGNORECASE
)
duration_rgx2 = re.compile(
    r"(-)?P(\d+)DT(\d{2})H(\d{2})M(\d{2})(?:\.(\d+))?S", re.IGNORECASE
)

ENUM_PROPERTIES = bool(find_spec("enum_properties"))
DJANGO_FILTERS = bool(find_spec("django_filters"))
DJANGO_REST_FRAMEWORK = bool(find_spec("rest_framework"))


def try_convert(primitive, value, raise_on_error=True):
    from dateutil.parser import ParserError

    try:
        return CONVERTERS[primitive](value)
    except (ValueError, TypeError, KeyError, ParserError, DecimalException) as err:
        if raise_on_error:
            raise ValueError(str(err)) from err
        return value


def str_to_timedelta(value):
    try:
        return timedelta(seconds=float(value))
    except ValueError:
        mtch = duration_rgx1.match(value) or duration_rgx2.match(value)
        if mtch:
            sign, days, hours, minutes, seconds, microseconds = mtch.groups()
            return (-1 if sign else 1) * timedelta(
                days=int(days),
                hours=int(hours),
                minutes=int(minutes),
                seconds=int(seconds),
                microseconds=int(microseconds or 0),
            )
        raise


def str_to_decimal(value):
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    if isinstance(value, str) and value:
        return Decimal(value)
    raise ValueError("Invalid decimal value")


def convert_date(value):
    from dateutil import parser

    return parser.parse(value).date()


def convert_datetime(value):
    from dateutil import parser

    return parser.parse(value)


def convert_time(value):
    from dateutil import parser

    return parser.parse(value).time()


CONVERTERS = {
    date: convert_date,
    datetime: convert_datetime,
    time: convert_time,
    timedelta: str_to_timedelta,
    Decimal: str_to_decimal,
}


###############################################################################
# ORACLE is buggy!

IGNORE_ORA_01843 = os.environ.get("IGNORE_ORA_01843", False) in [
    "true",
    "True",
    "1",
    "yes",
    "YES",
]
IGNORE_ORA_00932 = os.environ.get("IGNORE_ORA_00932", False) in [
    "true",
    "True",
    "1",
    "yes",
    "YES",
]
print(f"IGNORE_ORA_01843: {IGNORE_ORA_01843}")
print(f"IGNORE_ORA_00932: {IGNORE_ORA_00932}")
patch_oracle()
###############################################################################


APP1_DIR = Path(__file__).parent / "enum_prop"


class EnumTypeMixin:
    """
    We make use of inheritance to re-run lots of tests with vanilla Django choices
    enumerations and enumerations defined with integration with enum-properties.

    Since most of this code is identical, we use this mixin to resolve the correct
    type at the specific test in question.
    """

    fields = [
        "small_pos_int",
        "small_int",
        "pos_int",
        "int",
        "big_pos_int",
        "big_int",
        "constant",
        "text",
        "extern",
        "date_enum",
        "datetime_enum",
        "duration_enum",
        "time_enum",
        "decimal_enum",
        "dj_int_enum",
        "dj_text_enum",
        "non_strict_int",
        "non_strict_text",
        "no_coerce",
    ]

    @property
    def SmallPosIntEnum(self):
        return self.MODEL_CLASS._meta.get_field("small_pos_int").enum

    @property
    def SmallIntEnum(self):
        return self.MODEL_CLASS._meta.get_field("small_int").enum

    @property
    def PosIntEnum(self):
        return self.MODEL_CLASS._meta.get_field("pos_int").enum

    @property
    def IntEnum(self):
        return self.MODEL_CLASS._meta.get_field("int").enum

    @property
    def BigPosIntEnum(self):
        return self.MODEL_CLASS._meta.get_field("big_pos_int").enum

    @property
    def BigIntEnum(self):
        return self.MODEL_CLASS._meta.get_field("big_int").enum

    @property
    def Constants(self):
        return self.MODEL_CLASS._meta.get_field("constant").enum

    @property
    def TextEnum(self):
        return self.MODEL_CLASS._meta.get_field("text").enum

    @property
    def ExternEnum(self):
        return self.MODEL_CLASS._meta.get_field("extern").enum

    @property
    def DJIntEnum(self):
        return self.MODEL_CLASS._meta.get_field("dj_int_enum").enum

    @property
    def DJTextEnum(self):
        return self.MODEL_CLASS._meta.get_field("dj_text_enum").enum

    def enum_type(self, field_name):
        return self.MODEL_CLASS._meta.get_field(field_name).enum

    @property
    def DateEnum(self):
        return self.MODEL_CLASS._meta.get_field("date_enum").enum

    @property
    def DateTimeEnum(self):
        return self.MODEL_CLASS._meta.get_field("datetime_enum").enum

    @property
    def DurationEnum(self):
        return self.MODEL_CLASS._meta.get_field("duration_enum").enum

    @property
    def TimeEnum(self):
        return self.MODEL_CLASS._meta.get_field("time_enum").enum

    @property
    def DecimalEnum(self):
        return self.MODEL_CLASS._meta.get_field("decimal_enum").enum

    def enum_primitive(self, field_name):
        enum_type = self.enum_type(field_name)
        if enum_type in {
            self.SmallPosIntEnum,
            self.SmallIntEnum,
            self.IntEnum,
            self.PosIntEnum,
            self.BigIntEnum,
            self.BigPosIntEnum,
            self.DJIntEnum,
            self.ExternEnum,
        }:
            return int
        elif enum_type is self.Constants:
            return float
        elif enum_type in {self.TextEnum, self.DJTextEnum}:
            return str
        elif enum_type is self.DateEnum:
            return date
        elif enum_type is self.DateTimeEnum:
            return datetime
        elif enum_type is self.DurationEnum:
            return timedelta
        elif enum_type is self.TimeEnum:
            return time
        elif enum_type is self.DecimalEnum:
            return Decimal
        else:  # pragma: no cover
            raise RuntimeError(f"Missing enum type primitive for {enum_type}")


class FlagTypeMixin:
    """
    We make use of inheritance to re-run lots of tests with vanilla Django choices
    enumerations and enumerations defined with integration with enum-properties.

    Since most of this code is identical, we use this mixin to resolve the correct
    type at the specific test in question.
    """

    fields = ["small_flag", "flag", "flag_no_coerce", "big_flag"]

    @property
    def SmallPositiveFlagEnum(self):
        return self.enum_type("small_flag")

    @property
    def PositiveFlagEnum(self):
        return self.enum_type("flag")

    @property
    def BigPositiveFlagEnum(self):
        return self.enum_type("big_flag")

    def enum_type(self, field_name):
        return self.MODEL_CLASS._meta.get_field(field_name).enum

    def enum_primitive(self, field_name):
        return self.MODEL_CLASS._meta.get_field(field_name).primitive
