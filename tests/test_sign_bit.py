"""
Flag fields store their values two's complement in a signed integer column so
that every bit of the column, including the sign bit, is usable as a flag.
These tests cover that conversion and the field resolution rules that depend
on it. See https://github.com/django-commons/django-enum/issues/216
"""

import sys
from enum import IntFlag

from django.core.exceptions import ValidationError
from django.db import connection, transaction
from django.db.models import F, Value
from django.db.utils import IntegrityError
from django.test import SimpleTestCase, TestCase

from django_enum import EnumField
from django_enum.fields import (
    BigIntegerFlagField,
    ExtraBigIntegerFlagField,
    IntegerFlagField,
    SmallIntegerFlagField,
)
from tests.djenum.enums import BigTopBitFlagEnum, SmallTopBitFlagEnum, TopBitFlagEnum
from tests.djenum.models import EnumFlagTester

TOP_FIELDS = {
    "small_top": (SmallTopBitFlagEnum, 16),
    "top": (TopBitFlagEnum, 32),
    "big_top": (BigTopBitFlagEnum, 64),
}


def flags_of(bits: int) -> type[IntFlag]:
    """An IntFlag with its lowest and highest flag at the given width."""
    return IntFlag(f"Flags{bits}", {"LOW": 1, "HIGH": 1 << (bits - 1)})


class FieldResolutionTests(SimpleTestCase):
    def test_full_width_resolution(self):
        """The top bit of each column width is usable, only one past it widens."""
        for bits, field_cls, db_bits in [
            (16, SmallIntegerFlagField, 16),
            (17, IntegerFlagField, 32),
            (32, IntegerFlagField, 32),
            (33, BigIntegerFlagField, 64),
            (64, BigIntegerFlagField, 64),
            (65, ExtraBigIntegerFlagField, None),
        ]:
            field = EnumField(flags_of(bits))
            self.assertIsInstance(field, field_cls, bits)
            self.assertEqual(field.bit_length, bits)
            self.assertEqual(field.db_bit_length, db_bits)

    def test_non_flag_resolution(self):
        """
        Non-flag integer enumerations are unaffected: positive values still
        get positive columns, bit_length still overrides the width, and
        values that do not fit a bigint get the binary field.
        """
        from enum import IntEnum

        from django_enum.fields import (
            EnumExtraBigIntegerField,
            EnumPositiveIntegerField,
            EnumPositiveSmallIntegerField,
        )

        class Small(IntEnum):
            ONE = 1
            TWO = 2

        class Huge(IntEnum):
            ONE = 1
            BIG = 1 << 64

        self.assertIsInstance(EnumField(Small), EnumPositiveSmallIntegerField)
        self.assertEqual(EnumField(Small).bit_length, 2)
        # positive columns cannot use their sign bit, so 31 bits is the most
        # a 32 bit positive column holds
        wide = EnumField(Small, bit_length=31)
        self.assertIsInstance(wide, EnumPositiveIntegerField)
        self.assertEqual(wide.bit_length, 31)
        with self.assertRaises(AssertionError):
            EnumField(Huge, bit_length=32)
        huge = EnumField(Huge)
        self.assertIsInstance(huge, EnumExtraBigIntegerField)
        self.assertEqual(huge.bit_length, 65)

    def test_bit_length_override_widens(self):
        field = EnumField(flags_of(16), bit_length=32)
        self.assertIsInstance(field, IntegerFlagField)
        # the top flag of the enum is not the top bit of the column so it is
        # not converted
        self.assertEqual(field.get_prep_value(1 << 15), 1 << 15)

    def test_negative_flags_rejected(self):
        if sys.version_info >= (3, 15):
            # python 3.15 rewrites negative flag values before we can see them
            self.skipTest("negative flag values are rewritten on python >= 3.15")

        class Negative(IntFlag):
            ONE = 1
            TOP = -1 << 31

        with self.assertRaises(ValueError):
            EnumField(Negative)
        with self.assertRaises(ValueError):
            IntegerFlagField(Negative)

    def test_explicit_field_width_check(self):
        with self.assertRaises(ValueError):
            SmallIntegerFlagField(TopBitFlagEnum)
        with self.assertRaises(ValueError):
            IntegerFlagField(BigTopBitFlagEnum)
        # a wider column than necessary is fine, and the top flag of the enum
        # is then a plain positive value in the column
        field = IntegerFlagField(SmallTopBitFlagEnum)
        self.assertEqual(field.db_bit_length, 32)
        self.assertEqual(field.get_prep_value(SmallTopBitFlagEnum.FIVE), 1 << 15)

    def test_conversions(self):
        for name, (enum, bits) in TOP_FIELDS.items():
            field = EnumFlagTester._meta.get_field(name)
            top = 1 << (bits - 1)
            self.assertEqual(field.db_bit_length, bits)

            # outbound: unsigned flag value -> two's complement
            self.assertEqual(field.get_prep_value(enum.FIVE), -top)
            self.assertEqual(
                field.get_prep_value(enum.FIVE | enum.ONE), -top + enum.ONE
            )
            self.assertEqual(field.get_prep_value(enum.ONE), enum.ONE.value)
            self.assertEqual(field.get_prep_value(enum(0)), 0)
            self.assertIsNone(field.get_prep_value(None))
            self.assertEqual(
                field.get_db_prep_value(enum.FIVE | enum.TWO, connection),
                -top + enum.TWO,
            )

            # inbound: negative column value -> flag
            self.assertIs(field.from_db_value(-top, None, connection), enum.FIVE)
            self.assertEqual(
                field.from_db_value(-top + enum.ONE, None, connection),
                enum.FIVE | enum.ONE,
            )
            self.assertIs(
                field.from_db_value(enum.TWO.value, None, connection), enum.TWO
            )

            # legacy negative python values (django-enum 2.x spelled the top
            # bit as -1 << n) are accepted everywhere
            self.assertIs(field.to_python(-top), enum.FIVE)
            self.assertEqual(field.get_prep_value(-top), -top)
            self.assertEqual(field.get_prep_value(-top + enum.ONE), -top + enum.ONE)

            # negatives outside the column are not two's complement values
            self.assertEqual(field._to_unsigned(-top - 1), -top - 1)
            self.assertEqual(field._to_unsigned(-1), (1 << bits) - 1)

        # binary columns have no width and no conversion
        extra_big = EnumFlagTester._meta.get_field("extra_big_pos")
        self.assertIsNone(extra_big.db_bit_length)
        self.assertEqual(extra_big._to_unsigned(-1), -1)
        self.assertEqual(extra_big._to_signed(1 << 70), 1 << 70)


class StorageTests(TestCase):
    def raw(self, obj, name):
        field = EnumFlagTester._meta.get_field(name)
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT {field.column} FROM {EnumFlagTester._meta.db_table} "
                f"WHERE id = %s",
                [obj.pk],
            )
            return cursor.fetchone()[0]

    def test_storage_and_queries(self):
        for name, (enum, bits) in TOP_FIELDS.items():
            top = 1 << (bits - 1)
            obj = EnumFlagTester.objects.create(**{name: enum.FIVE | enum.ONE})
            alone = EnumFlagTester.objects.create(**{name: enum.FIVE})
            low = EnumFlagTester.objects.create(**{name: enum.ONE | enum.TWO})
            empty = EnumFlagTester.objects.create(**{name: enum(0)})

            # stored two's complement
            self.assertEqual(self.raw(obj, name), -top + enum.ONE)
            self.assertEqual(self.raw(alone, name), -top)
            self.assertEqual(self.raw(low, name), enum.ONE | enum.TWO)
            self.assertEqual(self.raw(empty, name), 0)

            # read back as flags
            obj.refresh_from_db()
            self.assertEqual(getattr(obj, name), enum.FIVE | enum.ONE)
            self.assertIsInstance(getattr(obj, name), enum)
            self.assertEqual(
                EnumFlagTester.objects.filter(pk=alone.pk)
                .values_list(name, flat=True)
                .first(),
                enum.FIVE,
            )

            qs = EnumFlagTester.objects.filter(
                pk__in=[obj.pk, alone.pk, low.pk, empty.pk]
            )

            self.assertEqual(qs.get(**{name: enum.FIVE}), alone)
            self.assertEqual(qs.get(**{name: enum.FIVE | enum.ONE}), obj)
            self.assertEqual(qs.get(**{name: -top}), alone)  # legacy spelling
            self.assertCountEqual(
                qs.filter(**{f"{name}__in": [enum.FIVE, enum(0)]}), [alone, empty]
            )
            self.assertCountEqual(
                qs.filter(**{f"{name}__has_any": enum.FIVE}), [obj, alone]
            )
            self.assertCountEqual(
                qs.filter(**{f"{name}__has_any": enum.FIVE | enum.TWO}),
                [obj, alone, low],
            )
            self.assertCountEqual(
                qs.filter(**{f"{name}__has_all": enum.FIVE | enum.ONE}), [obj]
            )
            self.assertCountEqual(
                qs.filter(**{f"{name}__has_all": enum.FIVE}), [obj, alone]
            )
            self.assertCountEqual(
                qs.exclude(**{f"{name}__has_any": enum.FIVE}), [low, empty]
            )

            # update() with a literal
            qs.filter(pk=low.pk).update(**{name: enum.FIVE | enum.THREE})
            self.assertEqual(self.raw(low, name), -top + enum.THREE)
            low.refresh_from_db()
            self.assertEqual(getattr(low, name), enum.FIVE | enum.THREE)

            # F() expressions need the flag wrapped so the field converts it
            field = EnumFlagTester._meta.get_field(name)
            qs.filter(pk=empty.pk).update(
                **{name: F(name).bitor(Value(enum.FIVE, output_field=field))}
            )
            self.assertEqual(self.raw(empty, name), -top)
            empty.refresh_from_db()
            self.assertEqual(getattr(empty, name), enum.FIVE)
            qs.filter(pk=obj.pk).update(
                **{name: F(name).bitand(Value(~enum.FIVE, output_field=field))}
            )
            obj.refresh_from_db()
            self.assertEqual(getattr(obj, name), enum.ONE)

    def test_legacy_negative_values(self):
        """
        Code written against django-enum 2.x may still pass the negative
        spelling of the top bit around, it maps onto the top flag.
        """
        for name, (enum, bits) in TOP_FIELDS.items():
            top = 1 << (bits - 1)
            obj = EnumFlagTester(**{name: -top})
            self.assertIs(getattr(obj, name), enum.FIVE)
            obj.save()
            obj.refresh_from_db()
            self.assertIs(getattr(obj, name), enum.FIVE)
            self.assertEqual(self.raw(obj, name), -top)
            self.assertEqual(
                EnumFlagTester.objects.get(
                    pk=obj.pk, **{name: -top + enum.ONE.value * 0}
                ),
                obj,
            )
            created = EnumFlagTester.objects.create(**{name: -top + enum.ONE})
            created.refresh_from_db()
            self.assertEqual(getattr(created, name), enum.FIVE | enum.ONE)

    def test_full_clean(self):
        for name, (enum, bits) in TOP_FIELDS.items():
            obj = EnumFlagTester(**{name: enum.FIVE | enum.ONE})
            obj.full_clean()
            obj.save()
            obj.full_clean()
            # KEEP boundary accepts extra bits, but they do not fit the column
            setattr(obj, name, 1 << bits)
            with self.assertRaises(ValidationError) as err:
                obj.full_clean()
            self.assertIn(name, err.exception.message_dict)


class ConstraintTests(TestCase):
    """
    Check constraints are bit mask checks expressed in two's complement so
    that they hold for values with the sign bit set.
    """

    def insert(self, field, literal):
        from tests.flag_constraints.models import FlagConstraintTestModel

        Model = FlagConstraintTestModel
        columns, values = [field.column], [str(literal)]
        for other in Model._meta.fields:
            default = getattr(other.default, "value", other.default)
            if other is not field and isinstance(default, int):
                columns.append(other.column)
                values.append(str(default))
        with transaction.atomic(), connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {Model._meta.db_table} ({','.join(columns)}) "
                f"VALUES ({','.join(values)})"
            )

    def check(self, name, valid, invalid):
        from tests.flag_constraints.models import FlagConstraintTestModel

        field = FlagConstraintTestModel._meta.get_field(name)
        for literal in valid:
            self.insert(field, literal)
        for literal in invalid:
            with self.assertRaises(IntegrityError, msg=f"{name}={literal}"):
                self.insert(field, literal)

    def test_top_bit_constraints(self):
        from tests.flag_constraints.enums import (
            StrictBigTopBitFlagEnum,
            StrictTopBitFlagEnum,
        )
        from tests.flag_constraints.models import FlagConstraintTestModel

        self.check(
            "strict_top",
            valid=[
                0,
                "NULL",
                2**13,
                2**14,
                2**13 + 2**14,
                -(2**15),  # VAL3
                -(2**15) + 2**13,  # VAL3 | VAL1
                -(2**15) + 2**13 + 2**14,  # VAL3 | VAL1 | VAL2
            ],
            invalid=[1, 2**12, 2**13 + 1, -1, -(2**15) + 1, 32767, -(2**15) + 2**12],
        )
        self.check(
            "strict_big_top",
            valid=[
                0,
                2**61,
                2**62,
                2**61 + 2**62,
                -(2**63),  # VAL3
                -(2**63) + 2**61,  # VAL3 | VAL1
            ],
            invalid=["NULL", 1, 2**60, 2**61 + 1, -1, -(2**63) + 1, -(2**63) + 2**60],
        )

        # the ORM round trips the top flag and full_clean() evaluates the
        # constraint in python without raising
        FlagConstraintTestModel.objects.all().delete()
        obj = FlagConstraintTestModel.objects.create(
            strict_top=StrictTopBitFlagEnum.VAL3 | StrictTopBitFlagEnum.VAL1,
            strict_big_top=StrictBigTopBitFlagEnum.VAL3,
        )
        obj.full_clean()
        obj.refresh_from_db()
        self.assertEqual(
            obj.strict_top, StrictTopBitFlagEnum.VAL3 | StrictTopBitFlagEnum.VAL1
        )
        self.assertIs(obj.strict_big_top, StrictBigTopBitFlagEnum.VAL3)
        self.assertEqual(
            FlagConstraintTestModel.objects.filter(
                strict_big_top__has_all=StrictBigTopBitFlagEnum.VAL3
            ).count(),
            1,
        )
