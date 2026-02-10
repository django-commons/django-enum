import pytest

pytest.importorskip("enum_properties")

import sys
from django.test import TestCase
from django_enum.choices import TextChoices
from enum import auto


@pytest.mark.skipif(sys.version_info < (3, 11), reason="Requires Python 3.11 or higher")
class TestAutoWithChoices(TestCase):
    def test_auto_with_choices(self):

        class MyTextChoices(TextChoices):
            custom_value: str

            FOO = auto(), "FOO Label", "foo123"
            BAR = auto(), "BAR Label", "bar123"

        self.assertEqual(MyTextChoices.FOO.value, "FOO")
        self.assertEqual(MyTextChoices.BAR.value, "BAR")

        self.assertEqual(MyTextChoices.FOO.label, "FOO Label")
        self.assertEqual(MyTextChoices.BAR.label, "BAR Label")

        self.assertEqual(MyTextChoices.FOO.custom_value, "foo123")
        self.assertEqual(MyTextChoices.BAR.custom_value, "bar123")

        class MyTextChoicesAutoOverride(TextChoices):
            def _generate_next_value_(name, start, count, last_values):
                return name.title() * 2

            custom_value: str

            FOO = auto(), "FOO Label", "foo123"
            BAR = auto(), "BAR Label", "bar123"

        self.assertEqual(MyTextChoicesAutoOverride.FOO.value, "FooFoo")
        self.assertEqual(MyTextChoicesAutoOverride.BAR.value, "BarBar")

        self.assertEqual(MyTextChoicesAutoOverride.FOO.label, "FOO Label")
        self.assertEqual(MyTextChoicesAutoOverride.BAR.label, "BAR Label")

        self.assertEqual(MyTextChoicesAutoOverride.FOO.custom_value, "foo123")
        self.assertEqual(MyTextChoicesAutoOverride.BAR.custom_value, "bar123")
