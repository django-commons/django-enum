import os
import sys
import pytest

# MySQL <8 does not support check constraints which is a problem for the
# migration tests - we have this check here to allow CI to disable them and
# still run the rest of the tests on mysql versions < 8 - remove this when
# 8 becomes the lowest version Django supports
DISABLE_CONSTRAINT_TESTS = os.environ.get("MYSQL_VERSION", "") == "5.7"
if DISABLE_CONSTRAINT_TESTS:
    pytest.skip(
        reason="MySQL 5.7 does not support check constraints", allow_module_level=True
    )


from django.test import TestCase
from tests.utils import EnumTypeMixin
from tests.djenum.models import EnumTester
from django_enum import EnumField
from django.db import connection, transaction


class ConstraintTests(EnumTypeMixin, TestCase):
    """Test that Django's choices types work as expected"""

    MODEL_CLASS = EnumTester

    def test_constraint_naming(self):
        from django_enum.fields import MAX_CONSTRAINT_NAME_LENGTH

        name = f"{self.MODEL_CLASS._meta.app_label}_EnumTester_small_pos_int_SmallPosIntEnum"

        self.assertEqual(
            EnumField.constraint_name(
                self.MODEL_CLASS, "small_pos_int", self.SmallPosIntEnum
            ),
            name
            if len(name) <= MAX_CONSTRAINT_NAME_LENGTH
            else name[len(name) - MAX_CONSTRAINT_NAME_LENGTH :],
        )

        self.assertEqual(
            EnumField.constraint_name(self.MODEL_CLASS, "small_int", self.SmallIntEnum),
            f"{self.MODEL_CLASS._meta.app_label}_EnumTester_small_int_SmallIntEnum",
        )

    def test_multi_primitive_constraints(self):
        from django.db import connection, transaction
        from django.db.utils import IntegrityError

        from tests.djenum.enums import MultiPrimitiveEnum, MultiWithNone
        from tests.djenum.models import MultiPrimitiveTestModel

        table_name = MultiPrimitiveTestModel._meta.db_table
        multi = MultiPrimitiveTestModel._meta.get_field("multi")
        multi_float = MultiPrimitiveTestModel._meta.get_field("multi_float")
        multi_none = MultiPrimitiveTestModel._meta.get_field("multi_none")
        multi_none_unconstrained = MultiPrimitiveTestModel._meta.get_field(
            "multi_none_unconstrained"
        )
        multi_unconstrained_non_strict = MultiPrimitiveTestModel._meta.get_field(
            "multi_unconstrained_non_strict"
        )

        def do_insert(db_field, db_insert):
            with connection.cursor() as db_cursor:
                with transaction.atomic():
                    if db_field is not multi_unconstrained_non_strict:
                        db_cursor.execute(
                            f"INSERT INTO {table_name} ({db_field.column}, "
                            f"{multi_unconstrained_non_strict.column}) VALUES "
                            f"({db_insert}, {getattr(multi_unconstrained_non_strict.default, 'value', multi_unconstrained_non_strict.default)})"
                        )
                        return
                    db_cursor.execute(
                        f"INSERT INTO {table_name} ({db_field.column}) VALUES ({db_insert})"
                    )

        for field, vals in [
            (
                multi,
                (
                    ("'1'", MultiPrimitiveEnum.VAL1),
                    ("'2.0'", MultiPrimitiveEnum.VAL2),
                    ("'3.0'", MultiPrimitiveEnum.VAL3),
                    ("'4.5'", MultiPrimitiveEnum.VAL4),
                    ("NULL", None),
                ),
            ),
            (
                multi_float,
                (
                    ("1.0", MultiPrimitiveEnum.VAL1),
                    ("2.0", MultiPrimitiveEnum.VAL2),
                    ("3.0", MultiPrimitiveEnum.VAL3),
                    ("4.5", MultiPrimitiveEnum.VAL4),
                    ("1", MultiPrimitiveEnum.VAL1),
                    ("2", MultiPrimitiveEnum.VAL2),
                    ("3", MultiPrimitiveEnum.VAL3),
                    ("NULL", None),
                ),
            ),
            (
                multi_none,
                (
                    ("'1'", MultiWithNone.VAL1),
                    ("'2.0'", MultiWithNone.VAL2),
                    ("'3.0'", MultiWithNone.VAL3),
                    ("'4.5'", MultiWithNone.VAL4),
                    ("NULL", MultiWithNone.NONE),
                ),
            ),
            (
                multi_none_unconstrained,
                (
                    ("'1'", MultiWithNone.VAL1),
                    ("'2.0'", MultiWithNone.VAL2),
                    ("'3.0'", MultiWithNone.VAL3),
                    ("'4.5'", MultiWithNone.VAL4),
                    ("NULL", MultiWithNone.NONE),
                ),
            ),
            (
                multi_unconstrained_non_strict,
                (
                    ("'1'", MultiPrimitiveEnum.VAL1),
                    ("'2.0'", MultiPrimitiveEnum.VAL2),
                    ("'3.0'", MultiPrimitiveEnum.VAL3),
                    ("'4.5'", MultiPrimitiveEnum.VAL4),
                ),
            ),
        ]:
            for insert, value in vals:
                MultiPrimitiveTestModel.objects.all().delete()

                do_insert(field, insert)

                if value == "NULL":
                    qry = MultiPrimitiveTestModel.objects.filter(
                        **{f"{field.name}__isnull": True}
                    )
                else:
                    qry = MultiPrimitiveTestModel.objects.filter(**{field.name: value})

                self.assertEqual(qry.count(), 1)
                self.assertEqual(getattr(qry.first(), field.name), value)

        MultiPrimitiveTestModel.objects.all().delete()

        for field, vals in [
            (multi, ("'1.0'", "2", "'4.6'", "'2'")),
            (multi_float, ("1.1", "2.1", "3.2", "4.6")),
            (multi_none, ("'1.0'", "2", "'4.6'", "'2'")),
            (
                multi_unconstrained_non_strict,
                ("NULL",),
            ),  # null=false still honored when unconstrained
        ]:
            for value in vals:
                # TODO it seems like Oracle allows nulls to be inserted
                #   directly when null=False??
                if (
                    field == multi_unconstrained_non_strict
                    and value == "NULL"
                    and connection.vendor == "oracle"
                ):
                    continue
                with self.assertRaises(IntegrityError):
                    do_insert(field, value)

        for field, vals in [
            (
                multi_none_unconstrained,
                (
                    ("'1.1'", "1.1"),
                    ("'2'", "2"),
                    ("'3.2'", "3.2"),
                    ("'4.6'", "4.6"),
                ),
            ),
        ]:
            for insert, value in vals:
                MultiPrimitiveTestModel.objects.all().delete()

                do_insert(field, insert)

                qry = MultiPrimitiveTestModel.objects.raw(
                    f"SELECT * FROM {table_name} WHERE {field.column} = {insert}"
                )
                with self.assertRaises(ValueError):
                    qry[0]

        for field, vals in [
            (
                multi_unconstrained_non_strict,
                (
                    ("'1.1'", "1.1"),
                    ("'2'", "2"),
                    ("'3.2'", "3.2"),
                    ("'4.6'", "4.6"),
                ),
            ),
        ]:
            for insert, value in vals:
                MultiPrimitiveTestModel.objects.all().delete()

                do_insert(field, insert)

                self.assertEqual(
                    getattr(
                        MultiPrimitiveTestModel.objects.filter(
                            **{field.name: value}
                        ).first(),
                        multi_unconstrained_non_strict.name,
                    ),
                    value,
                )

    def constraint_check(self, Model, field, values):
        from django.db.models.fields import NOT_PROVIDED
        from django.db.utils import IntegrityError

        table_name = Model._meta.db_table

        def do_insert(db_field, db_insert):
            with connection.cursor() as db_cursor:
                columns = [db_field.column]
                values = [db_insert]
                for field in Model._meta.fields:
                    if field is not db_field and field.default not in [
                        NOT_PROVIDED,
                        None,
                    ]:
                        columns.append(field.column)
                        values.append(
                            str(getattr(field.default, "value", field.default))
                        )

                with transaction.atomic():
                    db_cursor.execute(
                        f"INSERT INTO {table_name} ({','.join(columns)}) VALUES "
                        f"({','.join(values)})"
                    )

        for insert, value in values:
            Model.objects.all().delete()

            if value is IntegrityError:
                with self.assertRaises(IntegrityError):
                    do_insert(field, insert)
                continue

            do_insert(field, insert)

            if value == "NULL":
                qry = Model.objects.filter(**{f"{field.name}__isnull": True})
            else:
                qry = Model.objects.filter(**{field.name: value})

            self.assertEqual(qry.count(), 1)

            self.assertEqual(getattr(qry.first(), field.name), value)
            self.assertIsInstance(getattr(qry.first(), field.name), value.__class__)

    def test_default_flag_constraints(self):
        from tests.constraints.enums import IntFlagEnum
        from tests.constraints.models import FlagConstraintTestModel

        flag_field = FlagConstraintTestModel._meta.get_field("flag_field")
        flag_field_non_strict = FlagConstraintTestModel._meta.get_field(
            "flag_field_non_strict"
        )

        self.assertEqual(flag_field.bit_length, 15)
        self.assertEqual(flag_field_non_strict.bit_length, 15)

        self.assertEqual(IntFlagEnum(2**15), 2**15)
        self.assertIsInstance(IntFlagEnum(2**15), IntFlagEnum)

        self.assertEqual(IntFlagEnum(2**11), 2**11)
        self.assertIsInstance(IntFlagEnum(2**11), IntFlagEnum)

        self.assertIsInstance(IntFlagEnum(0), IntFlagEnum)

        for field in [flag_field, flag_field_non_strict]:
            self.constraint_check(
                FlagConstraintTestModel,
                field,
                (
                    ("'2048'", IntFlagEnum(2048)),
                    ("'4096'", IntFlagEnum.VAL1),
                    ("'8192'", IntFlagEnum.VAL2),
                    ("'16384'", IntFlagEnum.VAL3),
                    (
                        "'28672'",
                        (IntFlagEnum.VAL1 | IntFlagEnum.VAL2 | IntFlagEnum.VAL3),
                    ),
                    ("28673", IntFlagEnum(28673)),
                    ("32767", IntFlagEnum(32767)),
                    ("NULL", None),
                    ("0", IntFlagEnum(0)),
                ),
            )

    if sys.version_info >= (3, 11):

        def test_flag_constraints(self):
            from django.db.models import PositiveSmallIntegerField
            from django.db.utils import IntegrityError

            from tests.flag_constraints.enums import (
                ConformFlagEnum,
                EjectFlagEnum,
                KeepFlagEnum,
                StrictFlagEnum,
            )
            from tests.flag_constraints.models import (
                FlagConstraintTestModel,
            )

            keep_field = FlagConstraintTestModel._meta.get_field("keep")
            eject_field = FlagConstraintTestModel._meta.get_field("eject")
            eject_non_strict_field = FlagConstraintTestModel._meta.get_field(
                "eject_non_strict"
            )
            conform_field = FlagConstraintTestModel._meta.get_field("conform")
            strict_field = FlagConstraintTestModel._meta.get_field("strict")

            self.assertEqual(keep_field.bit_length, 15)
            self.assertEqual(eject_field.bit_length, 15)
            self.assertEqual(eject_non_strict_field.bit_length, 15)
            self.assertEqual(conform_field.bit_length, 15)
            self.assertEqual(strict_field.bit_length, 15)

            self.assertIsInstance(keep_field, PositiveSmallIntegerField)
            self.assertIsInstance(eject_field, PositiveSmallIntegerField)
            self.assertIsInstance(eject_non_strict_field, PositiveSmallIntegerField)
            self.assertIsInstance(conform_field, PositiveSmallIntegerField)
            self.assertIsInstance(strict_field, PositiveSmallIntegerField)

            # just some sanity checks to confirm how these enums behave

            # KEEP, maintains value and is an instance of the enum
            # No constraints on enum values in DB
            self.assertEqual(KeepFlagEnum(2**15), 2**15)
            self.assertIsInstance(KeepFlagEnum(2**15), KeepFlagEnum)
            self.assertEqual(KeepFlagEnum(2**11), 2**11)
            self.assertIsInstance(KeepFlagEnum(2**11), KeepFlagEnum)
            self.assertEqual(KeepFlagEnum(0), KeepFlagEnum(0))

            self.constraint_check(
                FlagConstraintTestModel,
                keep_field,
                (
                    ("'2048'", KeepFlagEnum(2048)),
                    ("'4096'", KeepFlagEnum.VAL1),
                    ("'8192'", KeepFlagEnum.VAL2),
                    ("'16384'", KeepFlagEnum.VAL3),
                    (
                        "'28672'",
                        (KeepFlagEnum.VAL1 | KeepFlagEnum.VAL2 | KeepFlagEnum.VAL3),
                    ),
                    ("28673", KeepFlagEnum(28673)),
                    ("32767", KeepFlagEnum(32767)),
                    ("NULL", None),
                    ("0", KeepFlagEnum(0)),
                ),
            )

            # EJECT, ejects value as an integer, EJECT and strict are
            # conceptually similar if strict = True, constrain enum to
            # bit_length, strict = False - no constraints

            self.assertEqual(EjectFlagEnum(2**15), 2**15)
            self.assertEqual(EjectFlagEnum(2**11), 2**11)
            self.assertNotIsInstance(EjectFlagEnum(2**15), EjectFlagEnum)
            self.assertNotIsInstance(EjectFlagEnum(2**11), EjectFlagEnum)
            self.assertIsInstance(EjectFlagEnum(0), EjectFlagEnum)

            self.constraint_check(
                FlagConstraintTestModel,
                eject_field,
                (
                    ("'2048'", IntegrityError),
                    ("'4096'", EjectFlagEnum.VAL1),
                    ("'8192'", EjectFlagEnum.VAL2),
                    ("'16384'", EjectFlagEnum.VAL3),
                    (
                        "'28672'",
                        (EjectFlagEnum.VAL1 | EjectFlagEnum.VAL2 | EjectFlagEnum.VAL3),
                    ),
                    ("28673", IntegrityError),
                    ("32767", IntegrityError),
                    ("NULL", IntegrityError),
                    ("0", EjectFlagEnum(0)),
                ),
            )

            self.constraint_check(
                FlagConstraintTestModel,
                eject_non_strict_field,
                (
                    ("'4096'", EjectFlagEnum.VAL1),
                    ("'8192'", EjectFlagEnum.VAL2),
                    ("'16384'", EjectFlagEnum.VAL3),
                    (
                        "'28672'",
                        (EjectFlagEnum.VAL1 | EjectFlagEnum.VAL2 | EjectFlagEnum.VAL3),
                    ),
                    ("28673", 28673),
                    ("32767", 32767),
                    ("NULL", IntegrityError),
                    ("0", EjectFlagEnum(0)),
                ),
            )

            FlagConstraintTestModel.objects.all().delete()
            FlagConstraintTestModel.objects.create(eject_non_strict=EjectFlagEnum(2048))
            FlagConstraintTestModel.objects.create(eject_non_strict=EjectFlagEnum(15))
            FlagConstraintTestModel.objects.create(
                eject_non_strict=EjectFlagEnum(32767)
            )
            for val in [2048, 15, 32767]:
                self.assertEqual(
                    FlagConstraintTestModel.objects.filter(
                        eject_non_strict=EjectFlagEnum(val)
                    ).count(),
                    1,
                )
                self.assertEqual(
                    FlagConstraintTestModel.objects.filter(
                        eject_non_strict=val
                    ).count(),
                    1,
                )

            # CONFORM, conforms value to the enum
            # constrain enum to bit_length - mostly because you want DB to be
            # searchable - otherwise unsearchable values may be entered
            self.assertEqual(ConformFlagEnum(2**15), 0)
            self.assertEqual(ConformFlagEnum(2**11), 0)
            self.assertIsInstance(ConformFlagEnum(2**15), ConformFlagEnum)
            self.assertIsInstance(ConformFlagEnum(2**11), ConformFlagEnum)
            self.assertEqual(ConformFlagEnum(0), 0)
            self.assertIsInstance(ConformFlagEnum(0), ConformFlagEnum)

            self.constraint_check(
                FlagConstraintTestModel,
                conform_field,
                (
                    ("'2048'", IntegrityError),
                    ("'4096'", ConformFlagEnum.VAL1),
                    ("'8192'", ConformFlagEnum.VAL2),
                    ("'16384'", ConformFlagEnum.VAL3),
                    (
                        "'28672'",
                        (
                            ConformFlagEnum.VAL1
                            | ConformFlagEnum.VAL2
                            | ConformFlagEnum.VAL3
                        ),
                    ),
                    ("28673", IntegrityError),
                    ("30720", IntegrityError),
                    ("32767", IntegrityError),
                    ("NULL", None),
                    ("0", ConformFlagEnum(0)),
                ),
            )
            FlagConstraintTestModel.objects.all().delete()
            FlagConstraintTestModel.objects.create(conform=ConformFlagEnum(2048))
            FlagConstraintTestModel.objects.create(conform=ConformFlagEnum(30720))
            FlagConstraintTestModel.objects.create(conform=ConformFlagEnum(32767))
            self.assertEqual(
                FlagConstraintTestModel.objects.filter(
                    conform=ConformFlagEnum(0)
                ).count(),
                1,
            )
            self.assertEqual(
                FlagConstraintTestModel.objects.filter(
                    conform=(
                        ConformFlagEnum.VAL1
                        | ConformFlagEnum.VAL2
                        | ConformFlagEnum.VAL3
                    )
                ).count(),
                2,
            )

            # STRICT, raises an error
            # constrain enum to bit_length
            with self.assertRaises(ValueError):
                StrictFlagEnum(2**15)

            with self.assertRaises(ValueError):
                StrictFlagEnum(2**11)

            self.assertIsInstance(StrictFlagEnum(0), StrictFlagEnum)

            self.constraint_check(
                FlagConstraintTestModel,
                strict_field,
                (
                    ("'2048'", IntegrityError),
                    ("'4096'", StrictFlagEnum.VAL1),
                    ("'8192'", StrictFlagEnum.VAL2),
                    ("'16384'", StrictFlagEnum.VAL3),
                    (
                        "'28672'",
                        (
                            StrictFlagEnum.VAL1
                            | StrictFlagEnum.VAL2
                            | StrictFlagEnum.VAL3
                        ),
                    ),
                    ("28673", IntegrityError),
                    ("32767", IntegrityError),
                    ("NULL", None),
                    ("0", StrictFlagEnum(0)),
                ),
            )
