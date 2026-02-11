from django.test import TestCase
from pathlib import Path
from decimal import Decimal
from django_enum.forms import EnumChoiceField
from django_enum.utils import choices


class TestEccentricEnums(TestCase):
    def test_primitive_resolution(self):
        from tests.djenum.models import MultiPrimitiveTestModel

        self.assertEqual(
            MultiPrimitiveTestModel._meta.get_field("multi").primitive, str
        )
        self.assertEqual(
            MultiPrimitiveTestModel._meta.get_field("multi_float").primitive, float
        )
        self.assertEqual(
            MultiPrimitiveTestModel._meta.get_field("multi_none").primitive, str
        )

    def test_multiple_primitives(self):
        from tests.djenum.models import (
            MultiPrimitiveEnum,
            MultiPrimitiveTestModel,
            MultiWithNone,
        )

        empty = MultiPrimitiveTestModel.objects.create()
        obj1 = MultiPrimitiveTestModel.objects.create(multi=MultiPrimitiveEnum.VAL1)
        obj2 = MultiPrimitiveTestModel.objects.create(multi=MultiPrimitiveEnum.VAL2)
        obj3 = MultiPrimitiveTestModel.objects.create(multi=MultiPrimitiveEnum.VAL3)
        obj4 = MultiPrimitiveTestModel.objects.create(multi=MultiPrimitiveEnum.VAL4)

        srch0 = MultiPrimitiveTestModel.objects.filter(multi__isnull=True)
        srch1 = MultiPrimitiveTestModel.objects.filter(multi=MultiPrimitiveEnum.VAL1)
        srch2 = MultiPrimitiveTestModel.objects.filter(multi=MultiPrimitiveEnum.VAL2)
        srch3 = MultiPrimitiveTestModel.objects.filter(multi=MultiPrimitiveEnum.VAL3)
        srch4 = MultiPrimitiveTestModel.objects.filter(multi=MultiPrimitiveEnum.VAL4)

        srch_v1 = MultiPrimitiveTestModel.objects.filter(
            multi=MultiPrimitiveEnum.VAL1.value
        )
        srch_v2 = MultiPrimitiveTestModel.objects.filter(
            multi=MultiPrimitiveEnum.VAL2.value
        )
        srch_v3 = MultiPrimitiveTestModel.objects.filter(
            multi=MultiPrimitiveEnum.VAL3.value
        )
        srch_v4 = MultiPrimitiveTestModel.objects.filter(
            multi=MultiPrimitiveEnum.VAL4.value
        )

        # search is also robust to symmetrical values
        srch_p1 = MultiPrimitiveTestModel.objects.filter(multi=1.0)
        srch_p2 = MultiPrimitiveTestModel.objects.filter(multi=Decimal("2.0"))
        srch_p3 = MultiPrimitiveTestModel.objects.filter(multi=3)
        srch_p4 = MultiPrimitiveTestModel.objects.filter(multi="4.5")

        with self.assertRaises(ValueError):
            MultiPrimitiveTestModel.objects.filter(multi=Decimal(1.1))

        with self.assertRaises(ValueError):
            MultiPrimitiveTestModel.objects.filter(multi="3.1")

        with self.assertRaises(ValueError):
            MultiPrimitiveTestModel.objects.filter(multi=4.6)

        self.assertEqual(srch0.count(), 1)
        self.assertEqual(srch1.count(), 1)
        self.assertEqual(srch2.count(), 1)
        self.assertEqual(srch3.count(), 1)
        self.assertEqual(srch4.count(), 1)
        self.assertEqual(srch_v1.count(), 1)
        self.assertEqual(srch_v2.count(), 1)
        self.assertEqual(srch_v3.count(), 1)
        self.assertEqual(srch_v4.count(), 1)
        self.assertEqual(srch_p1.count(), 1)
        self.assertEqual(srch_p2.count(), 1)
        self.assertEqual(srch_p3.count(), 1)
        self.assertEqual(srch_p4.count(), 1)

        self.assertEqual(srch0[0], empty)
        self.assertEqual(srch1[0], obj1)
        self.assertEqual(srch2[0], obj2)
        self.assertEqual(srch3[0], obj3)
        self.assertEqual(srch4[0], obj4)
        self.assertEqual(srch_p1[0], obj1)
        self.assertEqual(srch_p2[0], obj2)
        self.assertEqual(srch_p3[0], obj3)
        self.assertEqual(srch_p4[0], obj4)

        self.assertEqual(
            MultiPrimitiveTestModel.objects.filter(
                multi_float=MultiPrimitiveEnum.VAL2
            ).count(),
            5,
        )

        obj5 = MultiPrimitiveTestModel.objects.create(multi_none=None)

        nq0 = MultiPrimitiveTestModel.objects.filter(multi_none=MultiWithNone.NONE)
        nq1 = MultiPrimitiveTestModel.objects.filter(multi_none__isnull=True)
        nq2 = MultiPrimitiveTestModel.objects.filter(multi_none=None)
        self.assertEqual(nq0.count(), 1)
        self.assertEqual(nq1.count(), 1)
        self.assertEqual(nq2.count(), 1)
        self.assertTrue(nq0[0] == nq1[0] == nq2[0] == obj5)

    def test_enum_choice_field(self):
        from tests.djenum.enums import MultiPrimitiveEnum, MultiWithNone

        form_field1 = EnumChoiceField(MultiPrimitiveEnum)
        self.assertEqual(form_field1.choices, choices(MultiPrimitiveEnum))
        self.assertEqual(form_field1.primitive, str)

        form_field2 = EnumChoiceField(MultiPrimitiveEnum, primitive=float)
        self.assertEqual(form_field2.choices, choices(MultiPrimitiveEnum))
        self.assertEqual(form_field2.primitive, float)

        form_field3 = EnumChoiceField(MultiWithNone)
        self.assertEqual(form_field3.choices, choices(MultiWithNone))
        self.assertEqual(form_field3.primitive, str)

    def test_custom_primitive(self):
        from pathlib import PurePosixPath
        from tests.djenum.enums import PathEnum, StrProps, StrPropsEnum
        from tests.djenum.models import CustomPrimitiveTestModel

        obj = CustomPrimitiveTestModel.objects.create(
            path="/usr/local", str_props="str1"
        )
        self.assertEqual(obj.path, PathEnum.USR_LOCAL)
        self.assertEqual(obj.str_props, StrPropsEnum.STR1)

        obj2 = CustomPrimitiveTestModel.objects.create(
            path=PathEnum.USR, str_props=StrPropsEnum.STR2
        )
        self.assertEqual(obj2.path, PathEnum.USR)
        self.assertEqual(obj2.str_props, StrPropsEnum.STR2)

        obj3 = CustomPrimitiveTestModel.objects.create(
            path=PurePosixPath("/usr/local/bin"), str_props=StrProps("str3")
        )
        self.assertEqual(obj3.path, PathEnum.USR_LOCAL_BIN)
        self.assertEqual(obj3.str_props, StrPropsEnum.STR3)

        self.assertEqual(obj, CustomPrimitiveTestModel.objects.get(path="/usr/local"))
        self.assertEqual(obj, CustomPrimitiveTestModel.objects.get(str_props="str1"))

        self.assertEqual(obj2, CustomPrimitiveTestModel.objects.get(path=PathEnum.USR))
        self.assertEqual(
            obj2, CustomPrimitiveTestModel.objects.get(str_props=StrPropsEnum.STR2)
        )

        self.assertEqual(
            obj3,
            CustomPrimitiveTestModel.objects.get(path=PurePosixPath("/usr/local/bin")),
        )

        self.assertEqual(
            obj3,
            CustomPrimitiveTestModel.objects.get(str_props=StrProps("str3")),
        )

    def test_nullable_float(self):
        from tests.djenum.models import TestNullableFloat
        from tests.djenum.enums import NullableConstants

        obj = TestNullableFloat.objects.create()
        self.assertEqual(obj.nullable_float, NullableConstants.NONE)
        obj.refresh_from_db()
        self.assertEqual(obj.nullable_float, NullableConstants.NONE)

        obj.nullable_float = NullableConstants.PI
        obj.save()
        obj.refresh_from_db()
        self.assertEqual(obj.nullable_float, NullableConstants.PI)
