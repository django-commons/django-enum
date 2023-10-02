# Generated by Django 4.2.4 on 2023-10-02 16:10

import datetime
import pathlib
from decimal import Decimal

import django_enum.fields
import django_enum.tests.djenum.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminDisplayBug35',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_enum', django_enum.fields.EnumCharField(choices=[('V1', 'Value1'), ('V22', 'Value2'), ('V333', 'Value3'), ('D', 'Default')], default='V1', max_length=4)),
                ('int_enum', django_enum.fields.EnumPositiveSmallIntegerField(choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], default=2)),
                ('blank_int', django_enum.fields.EnumPositiveSmallIntegerField(choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], default=None, null=True)),
                ('blank_txt', django_enum.fields.EnumCharField(choices=[('V1', 'Value1'), ('V22', 'Value2'), ('V333', 'Value3'), ('D', 'Default')], default=None, max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BadDefault',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('non_strict_int', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], default=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomPrimitiveTestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', django_enum.fields.EnumCharField(choices=[(pathlib.PurePosixPath('/usr'), 'USR'), (pathlib.PurePosixPath('/usr/local'), 'USR_LOCAL'), (pathlib.PurePosixPath('/usr/local/bin'), 'USR_LOCAL_BIN')], max_length=14)),
                ('str_props', django_enum.fields.EnumCharField(choices=[(django_enum.tests.djenum.enums.StrProps('str1'), 'STR1'), (django_enum.tests.djenum.enums.StrProps('str2'), 'STR2'), (django_enum.tests.djenum.enums.StrProps('str3'), 'STR3')], max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='EmptyEnumValueTester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blank_text_enum', django_enum.fields.EnumCharField(choices=[('', 'Value1'), ('V22', 'Value2')], default='', max_length=3)),
                ('none_int_enum', django_enum.fields.EnumPositiveSmallIntegerField(choices=[(None, 'VALUE1'), (2, 'VALUE2')], default=None, null=True)),
                ('none_int_enum_non_null', django_enum.fields.EnumPositiveSmallIntegerField(choices=[(None, 'VALUE1'), (2, 'VALUE2')], null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnumFlagTester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_pos', django_enum.fields.SmallIntegerFlagField(blank=True, choices=[(1024, 'ONE'), (2048, 'TWO'), (4096, 'THREE'), (8192, 'FOUR'), (16384, 'FIVE')], db_index=True, default=None, null=True)),
                ('pos', django_enum.fields.IntegerFlagField(blank=True, choices=[(67108864, 'ONE'), (134217728, 'TWO'), (268435456, 'THREE'), (536870912, 'FOUR'), (1073741824, 'FIVE')], db_index=True, default=0)),
                ('big_pos', django_enum.fields.BigIntegerFlagField(blank=True, choices=[(288230376151711744, 'ONE'), (576460752303423488, 'TWO'), (1152921504606846976, 'THREE'), (2305843009213693952, 'FOUR'), (4611686018427387904, 'FIVE')], db_index=True, default=0)),
                ('extra_big_pos', django_enum.fields.ExtraBigIntegerFlagField(blank=True, choices=[(1, 'ONE'), (2, 'TWO'), (9223372036854775808, 'THREE'), (18446744073709551616, 'FOUR'), (36893488147419103232, 'FIVE')], db_index=True, default=0)),
                ('small_neg', django_enum.fields.EnumSmallIntegerField(blank=True, choices=[(-2048, 'ONE'), (-4096, 'TWO'), (-8192, 'THREE'), (-16384, 'FOUR'), (-32768, 'FIVE')], db_index=True, default=0)),
                ('neg', django_enum.fields.EnumIntegerField(blank=True, choices=[(-134217728, 'ONE'), (-268435456, 'TWO'), (-536870912, 'THREE'), (-1073741824, 'FOUR'), (-2147483648, 'FIVE')], db_index=True, default=0)),
                ('big_neg', django_enum.fields.EnumBigIntegerField(blank=True, choices=[(-576460752303423488, 'ONE'), (-1152921504606846976, 'TWO'), (-2305843009213693952, 'THREE'), (-4611686018427387904, 'FOUR'), (-9223372036854775808, 'FIVE')], db_index=True, default=0)),
                ('extra_big_neg', django_enum.fields.EnumExtraBigIntegerField(blank=True, choices=[(-1, 'ONE'), (-2, 'TWO'), (-18446744073709551616, 'THREE'), (-36893488147419103232, 'FOUR'), (-73786976294838206464, 'FIVE')], db_index=True, default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnumFlagTesterRelated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_pos', django_enum.fields.SmallIntegerFlagField(blank=True, choices=[(1024, 'ONE'), (2048, 'TWO'), (4096, 'THREE'), (8192, 'FOUR'), (16384, 'FIVE')], db_index=True, default=None, null=True)),
                ('pos', django_enum.fields.IntegerFlagField(blank=True, choices=[(67108864, 'ONE'), (134217728, 'TWO'), (268435456, 'THREE'), (536870912, 'FOUR'), (1073741824, 'FIVE')], db_index=True, default=0)),
                ('big_pos', django_enum.fields.BigIntegerFlagField(blank=True, choices=[(288230376151711744, 'ONE'), (576460752303423488, 'TWO'), (1152921504606846976, 'THREE'), (2305843009213693952, 'FOUR'), (4611686018427387904, 'FIVE')], db_index=True, default=0)),
                ('extra_big_pos', django_enum.fields.ExtraBigIntegerFlagField(blank=True, choices=[(1, 'ONE'), (2, 'TWO'), (9223372036854775808, 'THREE'), (18446744073709551616, 'FOUR'), (36893488147419103232, 'FIVE')], db_index=True, default=0)),
                ('small_neg', django_enum.fields.EnumSmallIntegerField(blank=True, choices=[(-2048, 'ONE'), (-4096, 'TWO'), (-8192, 'THREE'), (-16384, 'FOUR'), (-32768, 'FIVE')], db_index=True, default=0)),
                ('neg', django_enum.fields.EnumIntegerField(blank=True, choices=[(-134217728, 'ONE'), (-268435456, 'TWO'), (-536870912, 'THREE'), (-1073741824, 'FOUR'), (-2147483648, 'FIVE')], db_index=True, default=0)),
                ('big_neg', django_enum.fields.EnumBigIntegerField(blank=True, choices=[(-576460752303423488, 'ONE'), (-1152921504606846976, 'TWO'), (-2305843009213693952, 'THREE'), (-4611686018427387904, 'FOUR'), (-9223372036854775808, 'FIVE')], db_index=True, default=0)),
                ('extra_big_neg', django_enum.fields.EnumExtraBigIntegerField(blank=True, choices=[(-1, 'ONE'), (-2, 'TWO'), (-18446744073709551616, 'THREE'), (-36893488147419103232, 'FOUR'), (-73786976294838206464, 'FIVE')], db_index=True, default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnumTester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_pos_int', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], db_index=True, default=None, null=True)),
                ('small_int', django_enum.fields.EnumSmallIntegerField(blank=True, choices=[(-32768, 'Value -32768'), (0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], db_index=True, default=32767)),
                ('pos_int', django_enum.fields.EnumPositiveIntegerField(blank=True, choices=[(0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (2147483647, 'Value 2147483647')], db_index=True, default=2147483647)),
                ('int', django_enum.fields.EnumIntegerField(blank=True, choices=[(-2147483648, 'Value -2147483648'), (0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (2147483647, 'Value 2147483647')], db_index=True, null=True)),
                ('big_pos_int', django_enum.fields.EnumPositiveBigIntegerField(blank=True, choices=[(0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (2147483648, 'Value 2147483648')], db_index=True, default=None, null=True)),
                ('big_int', django_enum.fields.EnumBigIntegerField(blank=True, choices=[(-2147483649, 'Value -2147483649'), (1, 'Value 1'), (2, 'Value 2'), (2147483648, 'Value 2147483648')], db_index=True, default=-2147483649)),
                ('constant', django_enum.fields.EnumFloatField(blank=True, choices=[(3.141592653589793, 'Pi'), (2.71828, "Euler's Number"), (1.618033988749895, 'Golden Ratio')], db_index=True, default=None, null=True)),
                ('text', django_enum.fields.EnumCharField(choices=[('V1', 'Value1'), ('V22', 'Value2'), ('V333', 'Value3'), ('D', 'Default')], db_index=True, default=None, max_length=4, null=True)),
                ('extern', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(1, 'ONE'), (2, 'TWO'), (3, 'THREE')], db_index=True, default=None, null=True)),
                ('int_choice', models.IntegerField(blank=True, choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], default=1)),
                ('char_choice', models.CharField(blank=True, choices=[('A', 'First'), ('B', 'Second'), ('C', 'Third')], default='A', max_length=1)),
                ('int_field', models.IntegerField(blank=True, default=1)),
                ('float_field', models.FloatField(blank=True, default=1.5)),
                ('char_field', models.CharField(blank=True, default='A', max_length=1)),
                ('dj_int_enum', django_enum.fields.EnumPositiveSmallIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], default=1)),
                ('dj_text_enum', django_enum.fields.EnumCharField(choices=[('A', 'Label A'), ('B', 'Label B'), ('C', 'Label C')], default='A', max_length=1)),
                ('non_strict_int', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], default=5, null=True)),
                ('non_strict_text', django_enum.fields.EnumCharField(blank=True, choices=[('V1', 'Value1'), ('V22', 'Value2'), ('V333', 'Value3'), ('D', 'Default')], default='', max_length=12)),
                ('no_coerce', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], default=None, null=True)),
                ('date_enum', django_enum.fields.EnumDateField(blank=True, choices=[(datetime.date(1984, 8, 7), 'BRIAN'), (datetime.date(1989, 7, 27), 'EMMA'), (datetime.date(2016, 9, 9), 'HUGO')], default=datetime.date(1989, 7, 27))),
                ('datetime_enum', django_enum.fields.EnumDateTimeField(blank=True, choices=[(datetime.datetime(1980, 5, 18, 8, 32), 'ST_HELENS'), (datetime.datetime(1991, 6, 15, 20, 9), 'PINATUBO'), (datetime.datetime(2005, 8, 29, 5, 10), 'KATRINA')], default=None, null=True)),
                ('time_enum', django_enum.fields.EnumTimeField(blank=True, choices=[(datetime.time(17, 0), 'COB'), (datetime.time(12, 30), 'LUNCH'), (datetime.time(9, 0), 'MORNING')], default=None, null=True)),
                ('duration_enum', django_enum.fields.EnumDurationField(blank=True, choices=[(datetime.timedelta(days=1), 'DAY'), (datetime.timedelta(days=7), 'WEEK'), (datetime.timedelta(days=14), 'FORTNIGHT')], default=None, null=True)),
                ('decimal_enum', django_enum.fields.EnumDecimalField(blank=True, choices=[(Decimal('0.99'), 'ONE'), (Decimal('0.999'), 'TWO'), (Decimal('0.9999'), 'THREE'), (Decimal('99.9999'), 'FOUR'), (Decimal('999'), 'FIVE')], decimal_places=4, default=Decimal('0.9999'), max_digits=7)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='MultiPrimitiveTestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('multi', django_enum.fields.EnumCharField(blank=True, choices=[(1, 'VAL1'), ('2.0', 'VAL2'), (3.0, 'VAL3'), (Decimal('4.5'), 'VAL4')], default=None, max_length=3, null=True)),
                ('multi_float', django_enum.fields.EnumFloatField(blank=True, choices=[(1, 'VAL1'), ('2.0', 'VAL2'), (3.0, 'VAL3'), (Decimal('4.5'), 'VAL4')], default=2.0, null=True)),
                ('multi_none', django_enum.fields.EnumCharField(blank=True, choices=[(None, 'NONE'), (1, 'VAL1'), ('2.0', 'VAL2'), (3.0, 'VAL3'), (Decimal('4.5'), 'VAL4')], default='1', max_length=3, null=True)),
                ('multi_none_unconstrained', django_enum.fields.EnumCharField(blank=True, choices=[(None, 'NONE'), (1, 'VAL1'), ('2.0', 'VAL2'), (3.0, 'VAL3'), (Decimal('4.5'), 'VAL4')], default='1', max_length=3, null=True)),
                ('multi_unconstrained_non_strict', django_enum.fields.EnumCharField(blank=True, choices=[(1, 'VAL1'), ('2.0', 'VAL2'), (3.0, 'VAL3'), (Decimal('4.5'), 'VAL4')], default='1', max_length=3)),
            ],
        ),
        migrations.AddConstraint(
            model_name='multiprimitivetestmodel',
            constraint=models.CheckConstraint(check=models.Q(('multi__in', ['1', '2.0', '3.0', '4.5']), ('multi__isnull', True), _connector='OR'), name='um_tests_djenum_MultiPrimitiveTestModel_multi_MultiPrimitiveEnum'),
        ),
        migrations.AddConstraint(
            model_name='multiprimitivetestmodel',
            constraint=models.CheckConstraint(check=models.Q(('multi_float__in', [1.0, 2.0, 3.0, 4.5]), ('multi_float__isnull', True), _connector='OR'), name='ts_djenum_MultiPrimitiveTestModel_multi_float_MultiPrimitiveEnum'),
        ),
        migrations.AddConstraint(
            model_name='multiprimitivetestmodel',
            constraint=models.CheckConstraint(check=models.Q(('multi_none__in', [None, '1', '2.0', '3.0', '4.5']), ('multi_none__isnull', True), _connector='OR'), name='um_tests_djenum_MultiPrimitiveTestModel_multi_none_MultiWithNone'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('small_pos_int__in', [0, 2, 32767]), ('small_pos_int__isnull', True), _connector='OR'), name='jango_enum_tests_djenum_EnumTester_small_pos_int_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('small_int__in', [-32768, 0, 1, 2, 32767])), name='django_enum_tests_djenum_EnumTester_small_int_SmallIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('pos_int__in', [0, 1, 2, 2147483647])), name='django_enum_tests_djenum_EnumTester_pos_int_PosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('int__in', [-2147483648, 0, 1, 2, 2147483647]), ('int__isnull', True), _connector='OR'), name='django_enum_tests_djenum_EnumTester_int_IntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('big_pos_int__in', [0, 1, 2, 2147483648]), ('big_pos_int__isnull', True), _connector='OR'), name='django_enum_tests_djenum_EnumTester_big_pos_int_BigPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('big_int__in', [-2147483649, 1, 2, 2147483648])), name='django_enum_tests_djenum_EnumTester_big_int_BigIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('constant__in', [3.141592653589793, 2.71828, 1.618033988749895]), ('constant__isnull', True), _connector='OR'), name='django_enum_tests_djenum_EnumTester_constant_Constants'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('text__in', ['V1', 'V22', 'V333', 'D']), ('text__isnull', True), _connector='OR'), name='django_enum_tests_djenum_EnumTester_text_TextEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('extern__in', [1, 2, 3]), ('extern__isnull', True), _connector='OR'), name='django_enum_tests_djenum_EnumTester_extern_ExternEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('dj_int_enum__in', [1, 2, 3])), name='django_enum_tests_djenum_EnumTester_dj_int_enum_DJIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('dj_text_enum__in', ['A', 'B', 'C'])), name='django_enum_tests_djenum_EnumTester_dj_text_enum_DJTextEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('no_coerce__in', [0, 2, 32767]), ('no_coerce__isnull', True), _connector='OR'), name='django_enum_tests_djenum_EnumTester_no_coerce_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('date_enum__in', [datetime.date(1984, 8, 7), datetime.date(1989, 7, 27), datetime.date(2016, 9, 9)])), name='django_enum_tests_djenum_EnumTester_date_enum_DateEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('time_enum__in', [datetime.time(17, 0), datetime.time(12, 30), datetime.time(9, 0)]), ('time_enum__isnull', True), _connector='OR'), name='django_enum_tests_djenum_EnumTester_time_enum_TimeEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('duration_enum__in', [datetime.timedelta(days=1), datetime.timedelta(days=7), datetime.timedelta(days=14)]), ('duration_enum__isnull', True), _connector='OR'), name='django_enum_tests_djenum_EnumTester_duration_enum_DurationEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('decimal_enum__in', [Decimal('0.99'), Decimal('0.999'), Decimal('0.9999'), Decimal('99.9999'), Decimal('999')])), name='django_enum_tests_djenum_EnumTester_decimal_enum_DecimalEnum'),
        ),
        migrations.AddField(
            model_name='enumflagtesterrelated',
            name='related_flags',
            field=models.ManyToManyField(related_name='related_flags', to='django_enum_tests_djenum.enumflagtester'),
        ),
        migrations.AddConstraint(
            model_name='emptyenumvaluetester',
            constraint=models.CheckConstraint(check=models.Q(('blank_text_enum__in', ['', 'V22'])), name='_tests_djenum_EmptyEnumValueTester_blank_text_enum_BlankTextEnum'),
        ),
        migrations.AddConstraint(
            model_name='emptyenumvaluetester',
            constraint=models.CheckConstraint(check=models.Q(('none_int_enum__in', [None, 2]), ('none_int_enum__isnull', True), _connector='OR'), name='enum_tests_djenum_EmptyEnumValueTester_none_int_enum_NoneIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='emptyenumvaluetester',
            constraint=models.CheckConstraint(check=models.Q(('none_int_enum_non_null__in', [None, 2]), ('none_int_enum_non_null__isnull', True), _connector='OR'), name='s_djenum_EmptyEnumValueTester_none_int_enum_non_null_NoneIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='customprimitivetestmodel',
            constraint=models.CheckConstraint(check=models.Q(('path__in', ['/usr', '/usr/local', '/usr/local/bin'])), name='django_enum_tests_djenum_CustomPrimitiveTestModel_path_PathEnum'),
        ),
        migrations.AddConstraint(
            model_name='customprimitivetestmodel',
            constraint=models.CheckConstraint(check=models.Q(('str_props__in', ['str1', 'str2', 'str3'])), name='num_tests_djenum_CustomPrimitiveTestModel_str_props_StrPropsEnum'),
        ),
        migrations.AddConstraint(
            model_name='baddefault',
            constraint=models.CheckConstraint(check=models.Q(('non_strict_int__in', [0, 2, 32767]), ('non_strict_int__isnull', True), _connector='OR'), name='ango_enum_tests_djenum_BadDefault_non_strict_int_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='admindisplaybug35',
            constraint=models.CheckConstraint(check=models.Q(('text_enum__in', ['V1', 'V22', 'V333', 'D'])), name='django_enum_tests_djenum_AdminDisplayBug35_text_enum_TextEnum'),
        ),
        migrations.AddConstraint(
            model_name='admindisplaybug35',
            constraint=models.CheckConstraint(check=models.Q(('int_enum__in', [0, 2, 32767])), name='ngo_enum_tests_djenum_AdminDisplayBug35_int_enum_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='admindisplaybug35',
            constraint=models.CheckConstraint(check=models.Q(('blank_int__in', [0, 2, 32767]), ('blank_int__isnull', True), _connector='OR'), name='go_enum_tests_djenum_AdminDisplayBug35_blank_int_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='admindisplaybug35',
            constraint=models.CheckConstraint(check=models.Q(('blank_txt__in', ['V1', 'V22', 'V333', 'D']), ('blank_txt__isnull', True), _connector='OR'), name='django_enum_tests_djenum_AdminDisplayBug35_blank_txt_TextEnum'),
        ),
    ]
