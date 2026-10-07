import pytest

pytest.importorskip("enum_properties")
from tests.djenum.models import EnumTester
from django.core.exceptions import FieldError
from django.db.models import F
from tests.test_field_types import TestFieldTypeResolution
from tests.enum_prop.models import EnumTester
from tests.enum_prop.enums import GNSSConstellation, LargeBitField, LargeNegativeField
from tests.enum_prop.models import BitFieldModel, EnumTester


class TestFieldTypeResolutionProps(TestFieldTypeResolution):
    MODEL_CLASS = EnumTester

    def test_large_bitfields(self):
        tester = BitFieldModel.objects.create(
            bit_field_small=GNSSConstellation.GPS | GNSSConstellation.GLONASS
        )
        from django.db.models import BinaryField, SmallIntegerField

        self.assertIsInstance(
            tester._meta.get_field("bit_field_small"), SmallIntegerField
        )
        self.assertIsInstance(tester._meta.get_field("bit_field_large"), BinaryField)
        self.assertIsInstance(tester._meta.get_field("large_neg"), BinaryField)

        self.assertEqual(
            tester.bit_field_small,
            GNSSConstellation.GPS | GNSSConstellation.GLONASS,
        )
        self.assertEqual(tester.bit_field_large, None)
        self.assertEqual(tester.large_neg, LargeNegativeField.NEG_ONE)
        self.assertEqual(tester.no_default, LargeBitField(0))

        self.assertEqual(
            BitFieldModel.objects.filter(bit_field_large__isnull=True).count(), 1
        )
        tester.bit_field_large = LargeBitField.ONE | LargeBitField.TWO
        tester.save()
        self.assertEqual(
            BitFieldModel.objects.filter(bit_field_large__isnull=True).count(), 0
        )
        self.assertEqual(
            BitFieldModel.objects.filter(
                bit_field_large=LargeBitField.ONE | LargeBitField.TWO
            ).count(),
            1,
        )
        self.assertEqual(
            BitFieldModel.objects.filter(bit_field_large=LargeBitField.ONE).count(),
            0,
        )

        # todo this breaks on sqlite, integer overflow - what about other backends?
        # BitFieldModel.objects.filter(bit_field_large=LargeBitField.ONE | LargeBitField.TWO).update(bit_field_large=F('bit_field_large').bitand(~LargeBitField.TWO))

        BitFieldModel.objects.filter(
            bit_field_large=LargeBitField.ONE | LargeBitField.TWO
        ).update(bit_field_large=LargeBitField.ONE & ~LargeBitField.TWO)

        self.assertEqual(
            BitFieldModel.objects.filter(bit_field_large=LargeBitField.ONE).count(),
            1,
        )

        self.assertEqual(
            BitFieldModel.objects.filter(
                bit_field_small=GNSSConstellation.GPS | GNSSConstellation.GLONASS
            ).count(),
            1,
        )

        BitFieldModel.objects.filter(
            bit_field_small=GNSSConstellation.GPS | GNSSConstellation.GLONASS
        ).update(
            bit_field_small=F("bit_field_small").bitand(~GNSSConstellation.GLONASS)
        )

        self.assertEqual(
            BitFieldModel.objects.filter(
                bit_field_small=GNSSConstellation.GPS | GNSSConstellation.GLONASS
            ).count(),
            0,
        )

        self.assertEqual(
            BitFieldModel.objects.filter(bit_field_small=GNSSConstellation.GPS).count(),
            1,
        )

        tester2 = BitFieldModel.objects.create(
            bit_field_small=GNSSConstellation.GPS | GNSSConstellation.GLONASS,
            bit_field_large=LargeBitField.ONE | LargeBitField.TWO,
            large_neg=None,
        )

        # has_any and has_all are not supported on ExtraLarge bit fields
        with self.assertRaises(FieldError):
            BitFieldModel.objects.filter(bit_field_large__has_any=LargeBitField.ONE)

        with self.assertRaises(FieldError):
            BitFieldModel.objects.filter(
                bit_field_large__has_all=LargeBitField.ONE | LargeBitField.TWO
            )

        with self.assertRaises(FieldError):
            BitFieldModel.objects.filter(large_neg__has_any=LargeNegativeField.NEG_ONE)

        with self.assertRaises(FieldError):
            BitFieldModel.objects.filter(
                large_neg__has_all=LargeNegativeField.NEG_ONE | LargeNegativeField.ZERO
            )


TestFieldTypeResolution = None
