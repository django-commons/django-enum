# Generated by Django 4.2.4 on 2023-10-02 16:10

import datetime
from decimal import Decimal

import django_enum.fields
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
            name='BitFieldModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bit_field_small', django_enum.fields.SmallIntegerFlagField(choices=[(1, 'Gps'), (2, 'Glonass'), (4, 'Galileo'), (8, 'Beidou'), (16, 'Qzss')])),
                ('bit_field_large', django_enum.fields.ExtraBigIntegerFlagField(blank=True, choices=[(1, 'One'), (340282366920938463463374607431768211456, 'Two')], default=None, null=True)),
                ('bit_field_large_neg', django_enum.fields.EnumExtraBigIntegerField(choices=[(-340282366920938463463374607431768211456, 'Negative One'), (-1, 'ZERO')], default=-340282366920938463463374607431768211456, null=True)),
                ('no_default', django_enum.fields.ExtraBigIntegerFlagField(choices=[(1, 'One'), (340282366920938463463374607431768211456, 'Two')])),
            ],
        ),
        migrations.CreateModel(
            name='EnumFlagPropTester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_pos', django_enum.fields.SmallIntegerFlagField(blank=True, choices=[(1024, 'One'), (2048, 'Two'), (4096, 'Three'), (8192, 'Four'), (16384, 'Five')], db_index=True, default=None, null=True)),
                ('pos', django_enum.fields.IntegerFlagField(blank=True, choices=[(67108864, 'One'), (134217728, 'Two'), (268435456, 'Three'), (536870912, 'Four'), (1073741824, 'Five')], db_index=True, default=0)),
                ('big_pos', django_enum.fields.BigIntegerFlagField(blank=True, choices=[(288230376151711744, 'One'), (576460752303423488, 'Two'), (1152921504606846976, 'Three'), (2305843009213693952, 'Four'), (4611686018427387904, 'Five')], db_index=True, default=0)),
                ('extra_big_pos', django_enum.fields.ExtraBigIntegerFlagField(blank=True, choices=[(2305843009213693952, 'One'), (4611686018427387904, 'Two'), (9223372036854775808, 'Three'), (18446744073709551616, 'Four'), (36893488147419103232, 'Five')], db_index=True, default=0)),
                ('small_neg', django_enum.fields.EnumSmallIntegerField(blank=True, choices=[(-2048, 'One'), (-4096, 'Two'), (-8192, 'Three'), (-16384, 'Four'), (-32768, 'Five')], db_index=True, default=0)),
                ('neg', django_enum.fields.EnumIntegerField(blank=True, choices=[(-134217728, 'One'), (-268435456, 'Two'), (-536870912, 'Three'), (-1073741824, 'Four'), (-2147483648, 'Five')], db_index=True, default=0)),
                ('big_neg', django_enum.fields.EnumBigIntegerField(blank=True, choices=[(-576460752303423488, 'One'), (-1152921504606846976, 'Two'), (-2305843009213693952, 'Three'), (-4611686018427387904, 'Four'), (-9223372036854775808, 'Five')], db_index=True, default=0)),
                ('extra_big_neg', django_enum.fields.EnumExtraBigIntegerField(blank=True, choices=[(-4611686018427387904, 'One'), (-9223372036854775808, 'Two'), (-18446744073709551616, 'Three'), (-36893488147419103232, 'Four'), (-73786976294838206464, 'Five')], db_index=True, default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnumFlagPropTesterRelated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_pos', django_enum.fields.SmallIntegerFlagField(blank=True, choices=[(1024, 'One'), (2048, 'Two'), (4096, 'Three'), (8192, 'Four'), (16384, 'Five')], db_index=True, default=None, null=True)),
                ('pos', django_enum.fields.IntegerFlagField(blank=True, choices=[(67108864, 'One'), (134217728, 'Two'), (268435456, 'Three'), (536870912, 'Four'), (1073741824, 'Five')], db_index=True, default=0)),
                ('big_pos', django_enum.fields.BigIntegerFlagField(blank=True, choices=[(288230376151711744, 'One'), (576460752303423488, 'Two'), (1152921504606846976, 'Three'), (2305843009213693952, 'Four'), (4611686018427387904, 'Five')], db_index=True, default=0)),
                ('extra_big_pos', django_enum.fields.ExtraBigIntegerFlagField(blank=True, choices=[(2305843009213693952, 'One'), (4611686018427387904, 'Two'), (9223372036854775808, 'Three'), (18446744073709551616, 'Four'), (36893488147419103232, 'Five')], db_index=True, default=0)),
                ('small_neg', django_enum.fields.EnumSmallIntegerField(blank=True, choices=[(-2048, 'One'), (-4096, 'Two'), (-8192, 'Three'), (-16384, 'Four'), (-32768, 'Five')], db_index=True, default=0)),
                ('neg', django_enum.fields.EnumIntegerField(blank=True, choices=[(-134217728, 'One'), (-268435456, 'Two'), (-536870912, 'Three'), (-1073741824, 'Four'), (-2147483648, 'Five')], db_index=True, default=0)),
                ('big_neg', django_enum.fields.EnumBigIntegerField(blank=True, choices=[(-576460752303423488, 'One'), (-1152921504606846976, 'Two'), (-2305843009213693952, 'Three'), (-4611686018427387904, 'Four'), (-9223372036854775808, 'Five')], db_index=True, default=0)),
                ('extra_big_neg', django_enum.fields.EnumExtraBigIntegerField(blank=True, choices=[(-4611686018427387904, 'One'), (-9223372036854775808, 'Two'), (-18446744073709551616, 'Three'), (-36893488147419103232, 'Four'), (-73786976294838206464, 'Five')], db_index=True, default=0)),
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
                ('text', django_enum.fields.EnumCharField(blank=True, choices=[('V1', 'Value1'), ('V22', 'Value2'), ('V333', 'Value3'), ('D', 'Default')], db_index=True, default=None, max_length=4, null=True)),
                ('date_enum', django_enum.fields.EnumDateField(blank=True, choices=[(datetime.date(1984, 8, 7), 'Brian'), (datetime.date(1989, 7, 27), 'Emma'), (datetime.date(2016, 9, 9), 'Hugo')], default=datetime.date(1989, 7, 27))),
                ('datetime_enum', django_enum.fields.EnumDateTimeField(blank=True, choices=[(datetime.datetime(1980, 5, 18, 8, 32), 'Mount St. Helens'), (datetime.datetime(1991, 6, 15, 20, 9), 'Pinatubo'), (datetime.datetime(2005, 8, 29, 5, 10), 'Katrina')], default=None, null=True)),
                ('time_enum', django_enum.fields.EnumTimeField(blank=True, choices=[(datetime.time(17, 0), 'Close of Business'), (datetime.time(12, 30), 'Lunch'), (datetime.time(9, 0), 'Morning')], default=None, null=True)),
                ('duration_enum', django_enum.fields.EnumDurationField(blank=True, choices=[(datetime.timedelta(days=1), 'DAY'), (datetime.timedelta(days=7), 'WEEK'), (datetime.timedelta(days=14), 'FORTNIGHT')], default=None, null=True)),
                ('decimal_enum', django_enum.fields.EnumDecimalField(blank=True, choices=[(Decimal('0.99'), 'One'), (Decimal('0.999'), 'Two'), (Decimal('0.9999'), 'Three'), (Decimal('99.9999'), 'Four'), (Decimal('999'), 'Five')], decimal_places=4, default=Decimal('0.9999'), max_digits=7)),
                ('extern', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], db_index=True, default=None, null=True)),
                ('int_choice', models.IntegerField(blank=True, choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], default=1)),
                ('char_choice', models.CharField(blank=True, choices=[('A', 'First'), ('B', 'Second'), ('C', 'Third')], default='A', max_length=50)),
                ('int_field', models.IntegerField(blank=True, default=1)),
                ('float_field', models.FloatField(blank=True, default=1.5)),
                ('char_field', models.CharField(blank=True, default='A', max_length=1)),
                ('dj_int_enum', django_enum.fields.EnumPositiveSmallIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], default=1)),
                ('dj_text_enum', django_enum.fields.EnumCharField(choices=[('A', 'Label A'), ('B', 'Label B'), ('C', 'Label C')], default='A', max_length=1)),
                ('non_strict_int', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], default=5, null=True)),
                ('non_strict_text', django_enum.fields.EnumCharField(blank=True, choices=[('V1', 'Value1'), ('V22', 'Value2'), ('V333', 'Value3'), ('D', 'Default')], default='', max_length=12)),
                ('no_coerce', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], default=None, null=True)),
                ('gnss', django_enum.fields.SmallIntegerFlagField(blank=True, choices=[(1, 'Gps'), (2, 'Glonass'), (4, 'Galileo'), (8, 'Beidou'), (16, 'Qzss')], default=3)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txt_enum', django_enum.fields.EnumCharField(blank=True, choices=[('V0', 'Value 0'), ('V1', 'Value 1'), ('V2', 'Value 2')], max_length=2, null=True)),
                ('int_enum', django_enum.fields.EnumPositiveSmallIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three')])),
                ('color', django_enum.fields.EnumCharField(choices=[('R', 'Red'), ('G', 'Green'), ('B', 'Blue')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='NoCoercePerfCompare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_pos_int', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], db_index=True, default=None, null=True)),
                ('small_int', django_enum.fields.EnumSmallIntegerField(blank=True, choices=[(-32768, 'Value -32768'), (0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], db_index=True, default=32767)),
                ('pos_int', django_enum.fields.EnumPositiveIntegerField(blank=True, choices=[(0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (2147483647, 'Value 2147483647')], db_index=True, default=2147483647)),
                ('int', django_enum.fields.EnumIntegerField(blank=True, choices=[(-2147483648, 'Value -2147483648'), (0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (2147483647, 'Value 2147483647')], db_index=True, null=True)),
                ('big_pos_int', django_enum.fields.EnumPositiveBigIntegerField(blank=True, choices=[(0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (2147483648, 'Value 2147483648')], db_index=True, default=None, null=True)),
                ('big_int', django_enum.fields.EnumBigIntegerField(blank=True, choices=[(-2147483649, 'Value -2147483649'), (1, 'Value 1'), (2, 'Value 2'), (2147483648, 'Value 2147483648')], db_index=True, default=-2147483649)),
                ('constant', django_enum.fields.EnumFloatField(blank=True, choices=[(3.141592653589793, 'Pi'), (2.71828, "Euler's Number"), (1.618033988749895, 'Golden Ratio')], db_index=True, default=None, null=True)),
                ('text', django_enum.fields.EnumCharField(blank=True, choices=[('V1', 'Value1'), ('V22', 'Value2'), ('V333', 'Value3'), ('D', 'Default')], db_index=True, default=None, max_length=4, null=True)),
                ('int_choice', models.IntegerField(blank=True, choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], default=1)),
                ('char_choice', models.CharField(blank=True, choices=[('A', 'First'), ('B', 'Second'), ('C', 'Third')], default='A', max_length=1)),
                ('int_field', models.IntegerField(blank=True, default=1)),
                ('float_field', models.FloatField(blank=True, default=1.5)),
                ('char_field', models.CharField(blank=True, default='A', max_length=1)),
                ('dj_int_enum', django_enum.fields.EnumPositiveSmallIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], default=1)),
                ('dj_text_enum', django_enum.fields.EnumCharField(choices=[('A', 'Label A'), ('B', 'Label B'), ('C', 'Label C')], default='A', max_length=1)),
                ('non_strict_int', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], default=None, null=True)),
                ('non_strict_text', django_enum.fields.EnumCharField(blank=True, choices=[('V1', 'Value1'), ('V22', 'Value2'), ('V333', 'Value3'), ('D', 'Default')], default='', max_length=12)),
                ('no_coerce', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], default=None, null=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='PerfCompare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_pos_int', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], db_index=True, default=None, null=True)),
                ('small_int', models.SmallIntegerField(blank=True, choices=[(-32768, 'Value -32768'), (0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], db_index=True, default=32767)),
                ('pos_int', models.PositiveIntegerField(blank=True, choices=[(0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (2147483647, 'Value 2147483647')], db_index=True, default=2147483647)),
                ('int', models.IntegerField(blank=True, choices=[(-2147483648, 'Value -2147483648'), (0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (2147483647, 'Value 2147483647')], db_index=True, null=True)),
                ('big_pos_int', models.PositiveBigIntegerField(blank=True, choices=[(0, 'Value 0'), (1, 'Value 1'), (2, 'Value 2'), (2147483648, 'Value 2147483648')], db_index=True, default=None, null=True)),
                ('big_int', models.BigIntegerField(blank=True, choices=[(-2147483649, 'Value -2147483649'), (1, 'Value 1'), (2, 'Value 2'), (2147483648, 'Value 2147483648')], db_index=True, default=-2147483649)),
                ('constant', models.FloatField(blank=True, choices=[(3.141592653589793, 'Pi'), (2.71828, "Euler's Number"), (1.618033988749895, 'Golden Ratio')], db_index=True, default=None, null=True)),
                ('text', models.CharField(blank=True, choices=[('V1', 'Value1'), ('V22', 'Value2'), ('V333', 'Value3'), ('D', 'Default')], db_index=True, default=None, max_length=4, null=True)),
                ('int_choice', models.IntegerField(blank=True, choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], default=1)),
                ('char_choice', models.CharField(blank=True, choices=[('A', 'First'), ('B', 'Second'), ('C', 'Third')], default='A', max_length=1)),
                ('int_field', models.IntegerField(blank=True, default=1)),
                ('float_field', models.FloatField(blank=True, default=1.5)),
                ('char_field', models.CharField(blank=True, default='A', max_length=1)),
                ('dj_int_enum', models.PositiveSmallIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], default=1)),
                ('dj_text_enum', models.CharField(choices=[('A', 'Label A'), ('B', 'Label B'), ('C', 'Label C')], default='A', max_length=1)),
                ('non_strict_int', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], default=None, null=True)),
                ('non_strict_text', django_enum.fields.EnumCharField(blank=True, choices=[('V1', 'Value1'), ('V22', 'Value2'), ('V333', 'Value3'), ('D', 'Default')], default='', max_length=12)),
                ('no_coerce', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], default=None, null=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='SingleEnumPerf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_pos_int', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], db_index=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SingleFieldPerf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_pos_int', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], db_index=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SingleNoCoercePerf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_pos_int', django_enum.fields.EnumPositiveSmallIntegerField(blank=True, choices=[(0, 'Value 1'), (2, 'Value 2'), (32767, 'Value 32767')], db_index=True, default=None, null=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='singlenocoerceperf',
            constraint=models.CheckConstraint(check=models.Q(('small_pos_int__in', [0, 2, 32767]), ('small_pos_int__isnull', True), _connector='OR'), name='tests_enum_prop_SingleNoCoercePerf_small_pos_int_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='singleenumperf',
            constraint=models.CheckConstraint(check=models.Q(('small_pos_int__in', [0, 2, 32767]), ('small_pos_int__isnull', True), _connector='OR'), name='num_tests_enum_prop_SingleEnumPerf_small_pos_int_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='perfcompare',
            constraint=models.CheckConstraint(check=models.Q(('no_coerce__in', [0, 2, 32767]), ('no_coerce__isnull', True), _connector='OR'), name='jango_enum_tests_enum_prop_PerfCompare_no_coerce_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='nocoerceperfcompare',
            constraint=models.CheckConstraint(check=models.Q(('small_pos_int__in', [0, 2, 32767]), ('small_pos_int__isnull', True), _connector='OR'), name='ests_enum_prop_NoCoercePerfCompare_small_pos_int_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='nocoerceperfcompare',
            constraint=models.CheckConstraint(check=models.Q(('small_int__in', [-32768, 0, 1, 2, 32767])), name='_enum_tests_enum_prop_NoCoercePerfCompare_small_int_SmallIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='nocoerceperfcompare',
            constraint=models.CheckConstraint(check=models.Q(('pos_int__in', [0, 1, 2, 2147483647])), name='ango_enum_tests_enum_prop_NoCoercePerfCompare_pos_int_PosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='nocoerceperfcompare',
            constraint=models.CheckConstraint(check=models.Q(('int__in', [-2147483648, 0, 1, 2, 2147483647]), ('int__isnull', True), _connector='OR'), name='django_enum_tests_enum_prop_NoCoercePerfCompare_int_IntEnum'),
        ),
        migrations.AddConstraint(
            model_name='nocoerceperfcompare',
            constraint=models.CheckConstraint(check=models.Q(('big_pos_int__in', [0, 1, 2, 2147483648]), ('big_pos_int__isnull', True), _connector='OR'), name='um_tests_enum_prop_NoCoercePerfCompare_big_pos_int_BigPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='nocoerceperfcompare',
            constraint=models.CheckConstraint(check=models.Q(('big_int__in', [-2147483649, 1, 2, 2147483648])), name='ango_enum_tests_enum_prop_NoCoercePerfCompare_big_int_BigIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='nocoerceperfcompare',
            constraint=models.CheckConstraint(check=models.Q(('constant__in', [3.141592653589793, 2.71828, 1.618033988749895]), ('constant__isnull', True), _connector='OR'), name='ango_enum_tests_enum_prop_NoCoercePerfCompare_constant_Constants'),
        ),
        migrations.AddConstraint(
            model_name='nocoerceperfcompare',
            constraint=models.CheckConstraint(check=models.Q(('text__in', ['V1', 'V22', 'V333', 'D']), ('text__isnull', True), _connector='OR'), name='django_enum_tests_enum_prop_NoCoercePerfCompare_text_TextEnum'),
        ),
        migrations.AddConstraint(
            model_name='nocoerceperfcompare',
            constraint=models.CheckConstraint(check=models.Q(('dj_int_enum__in', [1, 2, 3])), name='o_enum_tests_enum_prop_NoCoercePerfCompare_dj_int_enum_DJIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='nocoerceperfcompare',
            constraint=models.CheckConstraint(check=models.Q(('dj_text_enum__in', ['A', 'B', 'C'])), name='enum_tests_enum_prop_NoCoercePerfCompare_dj_text_enum_DJTextEnum'),
        ),
        migrations.AddConstraint(
            model_name='nocoerceperfcompare',
            constraint=models.CheckConstraint(check=models.Q(('no_coerce__in', [0, 2, 32767]), ('no_coerce__isnull', True), _connector='OR'), name='um_tests_enum_prop_NoCoercePerfCompare_no_coerce_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='mymodel',
            constraint=models.CheckConstraint(check=models.Q(('txt_enum__in', ['V0', 'V1', 'V2']), ('txt_enum__isnull', True), _connector='OR'), name='django_enum_tests_enum_prop_MyModel_txt_enum_TextEnum'),
        ),
        migrations.AddConstraint(
            model_name='mymodel',
            constraint=models.CheckConstraint(check=models.Q(('int_enum__in', [1, 2, 3])), name='django_enum_tests_enum_prop_MyModel_int_enum_IntEnum'),
        ),
        migrations.AddConstraint(
            model_name='mymodel',
            constraint=models.CheckConstraint(check=models.Q(('color__in', ['R', 'G', 'B'])), name='django_enum_tests_enum_prop_MyModel_color_Color'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('small_pos_int__in', [0, 2, 32767]), ('small_pos_int__isnull', True), _connector='OR'), name='go_enum_tests_enum_prop_EnumTester_small_pos_int_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('small_int__in', [-32768, 0, 1, 2, 32767])), name='django_enum_tests_enum_prop_EnumTester_small_int_SmallIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('pos_int__in', [0, 1, 2, 2147483647])), name='django_enum_tests_enum_prop_EnumTester_pos_int_PosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('int__in', [-2147483648, 0, 1, 2, 2147483647]), ('int__isnull', True), _connector='OR'), name='django_enum_tests_enum_prop_EnumTester_int_IntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('big_pos_int__in', [0, 1, 2, 2147483648]), ('big_pos_int__isnull', True), _connector='OR'), name='django_enum_tests_enum_prop_EnumTester_big_pos_int_BigPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('big_int__in', [-2147483649, 1, 2, 2147483648])), name='django_enum_tests_enum_prop_EnumTester_big_int_BigIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('constant__in', [3.141592653589793, 2.71828, 1.618033988749895]), ('constant__isnull', True), _connector='OR'), name='django_enum_tests_enum_prop_EnumTester_constant_Constants'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('text__in', ['V1', 'V22', 'V333', 'D']), ('text__isnull', True), _connector='OR'), name='django_enum_tests_enum_prop_EnumTester_text_TextEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('date_enum__in', [datetime.date(1984, 8, 7), datetime.date(1989, 7, 27), datetime.date(2016, 9, 9)])), name='django_enum_tests_enum_prop_EnumTester_date_enum_DateEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('time_enum__in', [datetime.time(17, 0), datetime.time(12, 30), datetime.time(9, 0)]), ('time_enum__isnull', True), _connector='OR'), name='django_enum_tests_enum_prop_EnumTester_time_enum_TimeEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('duration_enum__in', [datetime.timedelta(days=1), datetime.timedelta(days=7), datetime.timedelta(days=14)]), ('duration_enum__isnull', True), _connector='OR'), name='jango_enum_tests_enum_prop_EnumTester_duration_enum_DurationEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('decimal_enum__in', [Decimal('0.99'), Decimal('0.999'), Decimal('0.9999'), Decimal('99.9999'), Decimal('999')])), name='django_enum_tests_enum_prop_EnumTester_decimal_enum_DecimalEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('extern__in', [1, 2, 3]), ('extern__isnull', True), _connector='OR'), name='django_enum_tests_enum_prop_EnumTester_extern_ExternEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('dj_int_enum__in', [1, 2, 3])), name='django_enum_tests_enum_prop_EnumTester_dj_int_enum_DJIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('dj_text_enum__in', ['A', 'B', 'C'])), name='django_enum_tests_enum_prop_EnumTester_dj_text_enum_DJTextEnum'),
        ),
        migrations.AddConstraint(
            model_name='enumtester',
            constraint=models.CheckConstraint(check=models.Q(('no_coerce__in', [0, 2, 32767]), ('no_coerce__isnull', True), _connector='OR'), name='django_enum_tests_enum_prop_EnumTester_no_coerce_SmallPosIntEnum'),
        ),
        migrations.AddField(
            model_name='enumflagproptesterrelated',
            name='related_flags',
            field=models.ManyToManyField(related_name='related_flags', to='django_enum_tests_enum_prop.enumflagproptester'),
        ),
        migrations.AddConstraint(
            model_name='admindisplaybug35',
            constraint=models.CheckConstraint(check=models.Q(('text_enum__in', ['V1', 'V22', 'V333', 'D'])), name='django_enum_tests_enum_prop_AdminDisplayBug35_text_enum_TextEnum'),
        ),
        migrations.AddConstraint(
            model_name='admindisplaybug35',
            constraint=models.CheckConstraint(check=models.Q(('int_enum__in', [0, 2, 32767])), name='_enum_tests_enum_prop_AdminDisplayBug35_int_enum_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='admindisplaybug35',
            constraint=models.CheckConstraint(check=models.Q(('blank_int__in', [0, 2, 32767]), ('blank_int__isnull', True), _connector='OR'), name='enum_tests_enum_prop_AdminDisplayBug35_blank_int_SmallPosIntEnum'),
        ),
        migrations.AddConstraint(
            model_name='admindisplaybug35',
            constraint=models.CheckConstraint(check=models.Q(('blank_txt__in', ['V1', 'V22', 'V333', 'D']), ('blank_txt__isnull', True), _connector='OR'), name='django_enum_tests_enum_prop_AdminDisplayBug35_blank_txt_TextEnum'),
        ),
    ]
