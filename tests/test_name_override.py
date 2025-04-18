from django.test import TestCase
from pathlib import Path
from decimal import Decimal
from django_enum.forms import EnumChoiceField
from django_enum.utils import choices


class TestNameOverride(TestCase):
    """
    https://github.com/django-commons/django-enum/issues/77
    """

    def test_name_override(self):
        from tests.djenum.models import NameOverrideTest

        self.assertEqual(NameOverrideTest._meta.get_field("enum_field").primitive, str)

        NameOverrideTest.objects.create(enum_field="V1")
        obj = NameOverrideTest.objects.first()
        self.assertEqual(obj.enum_field, "V1")
        self.assertEqual(obj.get_enum_field_display(), "Value 1")
