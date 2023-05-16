# Generated by Django 4.2.1 on 2023-05-16 16:00

from django.db import migrations, models
import django_enum.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BitFieldExample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observables', django_enum.fields.FlagExtraBigIntegerField(choices=[(1, 'C1C'), (2, 'C1S'), (4, 'C1L'), (8, 'C1X'), (16, 'C1P'), (32, 'C1W'), (64, 'C1Y'), (128, 'C1M'), (256, 'C2C'), (512, 'C2D'), (1024, 'C2S'), (2048, 'C2L'), (4096, 'C2X'), (8192, 'C2P'), (16384, 'C2W'), (32768, 'C2Y'), (65536, 'C2M'), (131072, 'C5I'), (262144, 'C5Q'), (524288, 'C5X'), (1048576, 'L1C'), (2097152, 'L1S'), (4194304, 'L1L'), (8388608, 'L1X'), (16777216, 'L1P'), (33554432, 'L1W'), (67108864, 'L1Y'), (134217728, 'L1M'), (268435456, 'L1N'), (536870912, 'L2C'), (1073741824, 'L2D'), (2147483648, 'L2S'), (4294967296, 'L2L'), (8589934592, 'L2X'), (17179869184, 'L2P'), (34359738368, 'L2W'), (68719476736, 'L2Y'), (137438953472, 'L2M'), (274877906944, 'L2N'), (549755813888, 'L5I'), (1099511627776, 'L5Q'), (2199023255552, 'L5X'), (4398046511104, 'D1C'), (8796093022208, 'D1S'), (17592186044416, 'D1L'), (35184372088832, 'D1X'), (70368744177664, 'D1P'), (140737488355328, 'D1W'), (281474976710656, 'D1Y'), (562949953421312, 'D1M'), (1125899906842624, 'D1N'), (2251799813685248, 'D2C'), (4503599627370496, 'D2D'), (9007199254740992, 'D2S'), (18014398509481984, 'D2L'), (36028797018963968, 'D2X'), (72057594037927936, 'D2P'), (144115188075855872, 'D2W'), (288230376151711744, 'D2Y'), (576460752303423488, 'D2M'), (1152921504606846976, 'D2N'), (2305843009213693952, 'D5I'), (4611686018427387904, 'D5Q'), (9223372036854775808, 'D5X'), (18446744073709551616, 'S1C'), (36893488147419103232, 'S1S'), (73786976294838206464, 'S1L'), (147573952589676412928, 'S1X'), (295147905179352825856, 'S1P'), (590295810358705651712, 'S1W'), (1180591620717411303424, 'S1Y'), (2361183241434822606848, 'S1M'), (4722366482869645213696, 'S1N'), (9444732965739290427392, 'S2C'), (18889465931478580854784, 'S2D'), (37778931862957161709568, 'S2S'), (75557863725914323419136, 'S2L'), (151115727451828646838272, 'S2X'), (302231454903657293676544, 'S2P'), (604462909807314587353088, 'S2W'), (1208925819614629174706176, 'S2Y'), (2417851639229258349412352, 'S2M'), (4835703278458516698824704, 'S2N'), (9671406556917033397649408, 'S5I'), (19342813113834066795298816, 'S5Q'), (38685626227668133590597632, 'S5X')])),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', django_enum.fields.EnumPositiveSmallIntegerField(choices=[(1, 'Streets'), (2, 'Outdoors'), (3, 'Light'), (4, 'Dark'), (5, 'Satellite'), (6, 'Satellite Streets'), (7, 'Navigation Day'), (8, 'Navigation Night')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txt_enum', django_enum.fields.EnumCharField(blank=True, choices=[('V0', 'Value 0'), ('V1', 'Value 1'), ('V2', 'Value 2')], max_length=2, null=True)),
                ('int_enum', django_enum.fields.EnumPositiveSmallIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three')])),
            ],
        ),
        migrations.CreateModel(
            name='NoCoerceExample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('non_strict', django_enum.fields.EnumCharField(choices=[('1', 'One'), ('2', 'Two')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='StrictExample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('non_strict', django_enum.fields.EnumCharField(choices=[('1', 'One'), ('2', 'Two')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TextChoicesExample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', django_enum.fields.EnumCharField(choices=[('R', 'Red'), ('G', 'Green'), ('B', 'Blue')], max_length=1)),
            ],
        ),
    ]
