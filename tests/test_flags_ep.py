import pytest

pytest.importorskip("enum_properties")
from tests.test_flags import FlagTests
from tests.enum_prop.models import EnumFlagPropTester, EnumFlagPropTesterRelated
from django_enum.utils import choices, names


class FlagTestsProp(FlagTests):
    MODEL_CLASS = EnumFlagPropTester
    RELATED_CLASS = EnumFlagPropTesterRelated

    def test_prop_enum(self):
        from tests.enum_prop.enums import (
            GNSSConstellation,
            SmallTopBitFlagEnum,
            SmallPositiveFlagEnum,
        )

        self.assertEqual(GNSSConstellation.GPS, GNSSConstellation("gps"))
        self.assertEqual(GNSSConstellation.GLONASS, GNSSConstellation("GLONASS"))
        self.assertEqual(GNSSConstellation.GALILEO, GNSSConstellation("galileo"))
        self.assertEqual(GNSSConstellation.BEIDOU, GNSSConstellation("BeiDou"))
        self.assertEqual(GNSSConstellation.QZSS, GNSSConstellation("qzss"))

        self.assertEqual(choices(SmallTopBitFlagEnum), SmallTopBitFlagEnum.choices)
        self.assertEqual(names(SmallTopBitFlagEnum), SmallTopBitFlagEnum.names)

        self.assertEqual(choices(SmallPositiveFlagEnum), SmallPositiveFlagEnum.choices)
        self.assertEqual(names(SmallPositiveFlagEnum), SmallPositiveFlagEnum.names)


FlagTests = None
