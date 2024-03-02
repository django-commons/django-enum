# Generated by Django 5.0.2 on 2024-03-02 16:48

from django.db import migrations, models

import django_enum.fields
import django_enum.tests.djenum.enums


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DBDefaultTester",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "small_pos_int",
                    django_enum.fields.EnumPositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (0, "Value 1"),
                            (2, "Value 2"),
                            (32767, "Value 32767"),
                        ],
                        db_default=None,
                        null=True,
                    ),
                ),
                (
                    "small_int",
                    django_enum.fields.EnumSmallIntegerField(
                        blank=True,
                        choices=[
                            (-32768, "Value -32768"),
                            (0, "Value 0"),
                            (1, "Value 1"),
                            (2, "Value 2"),
                            (32767, "Value 32767"),
                        ],
                        db_default=32767,
                    ),
                ),
                (
                    "pos_int",
                    django_enum.fields.EnumPositiveIntegerField(
                        blank=True,
                        choices=[
                            (0, "Value 0"),
                            (1, "Value 1"),
                            (2, "Value 2"),
                            (2147483647, "Value 2147483647"),
                        ],
                        db_default=2147483647,
                    ),
                ),
                (
                    "int",
                    django_enum.fields.EnumIntegerField(
                        blank=True,
                        choices=[
                            (-2147483648, "Value -2147483648"),
                            (0, "Value 0"),
                            (1, "Value 1"),
                            (2, "Value 2"),
                            (2147483647, "Value 2147483647"),
                        ],
                        db_default=-2147483648,
                        null=True,
                    ),
                ),
                (
                    "big_pos_int",
                    django_enum.fields.EnumPositiveBigIntegerField(
                        blank=True,
                        choices=[
                            (0, "Value 0"),
                            (1, "Value 1"),
                            (2, "Value 2"),
                            (2147483648, "Value 2147483648"),
                        ],
                        db_default=None,
                        null=True,
                    ),
                ),
                (
                    "big_int",
                    django_enum.fields.EnumBigIntegerField(
                        blank=True,
                        choices=[
                            (-2147483649, "Value -2147483649"),
                            (1, "Value 1"),
                            (2, "Value 2"),
                            (2147483648, "Value 2147483648"),
                        ],
                        db_default=-2147483649,
                    ),
                ),
                (
                    "constant",
                    django_enum.fields.EnumFloatField(
                        blank=True,
                        choices=[
                            (3.141592653589793, "Pi"),
                            (2.71828, "Euler's Number"),
                            (1.618033988749895, "Golden Ratio"),
                        ],
                        db_default=1.618033988749895,
                        null=True,
                    ),
                ),
                (
                    "text",
                    django_enum.fields.EnumCharField(
                        blank=True,
                        choices=[
                            ("V1", "Value1"),
                            ("V22", "Value2"),
                            ("V333", "Value3"),
                            ("D", "Default"),
                        ],
                        db_default="",
                        max_length=4,
                    ),
                ),
                (
                    "doubled_text",
                    django_enum.fields.EnumCharField(
                        blank=True,
                        choices=[
                            ("V1", "Value1"),
                            ("V22", "Value2"),
                            ("V333", "Value3"),
                            ("D", "Default"),
                        ],
                        db_default="db_default",
                        default="",
                        max_length=10,
                    ),
                ),
                (
                    "doubled_text_strict",
                    django_enum.fields.EnumCharField(
                        blank=True,
                        choices=[
                            ("V1", "Value1"),
                            ("V22", "Value2"),
                            ("V333", "Value3"),
                            ("D", "Default"),
                        ],
                        db_default="V22",
                        default="D",
                        max_length=10,
                    ),
                ),
                (
                    "char_field",
                    models.CharField(
                        blank=True, db_default="db_default", max_length=10
                    ),
                ),
                (
                    "doubled_char_field",
                    models.CharField(
                        blank=True,
                        db_default="db_default",
                        default="default",
                        max_length=10,
                    ),
                ),
                (
                    "extern",
                    django_enum.fields.EnumPositiveSmallIntegerField(
                        blank=True,
                        choices=[(1, "ONE"), (2, "TWO"), (3, "THREE")],
                        db_default=django_enum.tests.djenum.enums.ExternEnum["THREE"],
                        null=True,
                    ),
                ),
                (
                    "dj_int_enum",
                    django_enum.fields.EnumPositiveSmallIntegerField(
                        choices=[(1, "One"), (2, "Two"), (3, "Three")], db_default=1
                    ),
                ),
                (
                    "dj_text_enum",
                    django_enum.fields.EnumCharField(
                        choices=[("A", "Label A"), ("B", "Label B"), ("C", "Label C")],
                        db_default="A",
                        max_length=1,
                    ),
                ),
                (
                    "non_strict_int",
                    django_enum.fields.EnumPositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (0, "Value 1"),
                            (2, "Value 2"),
                            (32767, "Value 32767"),
                        ],
                        db_default=5,
                        null=True,
                    ),
                ),
                (
                    "non_strict_text",
                    django_enum.fields.EnumCharField(
                        blank=True,
                        choices=[
                            ("V1", "Value1"),
                            ("V22", "Value2"),
                            ("V333", "Value3"),
                            ("D", "Default"),
                        ],
                        db_default="arbitrary",
                        max_length=12,
                    ),
                ),
                (
                    "no_coerce",
                    django_enum.fields.EnumPositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (0, "Value 1"),
                            (2, "Value 2"),
                            (32767, "Value 32767"),
                        ],
                        db_default=2,
                        null=True,
                    ),
                ),
                (
                    "no_coerce_value",
                    django_enum.fields.EnumPositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (0, "Value 1"),
                            (2, "Value 2"),
                            (32767, "Value 32767"),
                        ],
                        db_default=32767,
                        null=True,
                    ),
                ),
                (
                    "no_coerce_none",
                    django_enum.fields.EnumPositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (0, "Value 1"),
                            (2, "Value 2"),
                            (32767, "Value 32767"),
                        ],
                        db_default=None,
                        null=True,
                    ),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("small_pos_int__in", [0, 2, 32767]),
                    ("small_pos_int__isnull", True),
                    _connector="OR",
                ),
                name="m_tests_db_default_DBDefaultTester_small_pos_int_SmallPosIntEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(("small_int__in", [-32768, 0, 1, 2, 32767])),
                name="ngo_enum_tests_db_default_DBDefaultTester_small_int_SmallIntEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(("pos_int__in", [0, 1, 2, 2147483647])),
                name="django_enum_tests_db_default_DBDefaultTester_pos_int_PosIntEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("int__in", [-2147483648, 0, 1, 2, 2147483647]),
                    ("int__isnull", True),
                    _connector="OR",
                ),
                name="django_enum_tests_db_default_DBDefaultTester_int_IntEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("big_pos_int__in", [0, 1, 2, 2147483648]),
                    ("big_pos_int__isnull", True),
                    _connector="OR",
                ),
                name="_enum_tests_db_default_DBDefaultTester_big_pos_int_BigPosIntEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(("big_int__in", [-2147483649, 1, 2, 2147483648])),
                name="django_enum_tests_db_default_DBDefaultTester_big_int_BigIntEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("constant__in", [3.141592653589793, 2.71828, 1.618033988749895]),
                    ("constant__isnull", True),
                    _connector="OR",
                ),
                name="django_enum_tests_db_default_DBDefaultTester_constant_Constants",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(("doubled_text_strict__in", ["V1", "V22", "V333", "D"])),
                name="um_tests_db_default_DBDefaultTester_doubled_text_strict_TextEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("extern__in", [1, 2, 3]), ("extern__isnull", True), _connector="OR"
                ),
                name="django_enum_tests_db_default_DBDefaultTester_extern_ExternEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(("dj_int_enum__in", [1, 2, 3])),
                name="ango_enum_tests_db_default_DBDefaultTester_dj_int_enum_DJIntEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(("dj_text_enum__in", ["A", "B", "C"])),
                name="go_enum_tests_db_default_DBDefaultTester_dj_text_enum_DJTextEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("no_coerce__in", [0, 2, 32767]),
                    ("no_coerce__isnull", True),
                    _connector="OR",
                ),
                name="_enum_tests_db_default_DBDefaultTester_no_coerce_SmallPosIntEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("no_coerce_value__in", [0, 2, 32767]),
                    ("no_coerce_value__isnull", True),
                    _connector="OR",
                ),
                name="tests_db_default_DBDefaultTester_no_coerce_value_SmallPosIntEnum",
            ),
        ),
        migrations.AddConstraint(
            model_name="dbdefaulttester",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("no_coerce_none__in", [0, 2, 32767]),
                    ("no_coerce_none__isnull", True),
                    _connector="OR",
                ),
                name="_tests_db_default_DBDefaultTester_no_coerce_none_SmallPosIntEnum",
            ),
        ),
    ]
