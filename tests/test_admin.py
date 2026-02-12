import pytest
import django
from django.db.models.fields import BLANK_CHOICE_DASH
import typing as t
import os
from enum import Enum, Flag
from tests.utils import EnumTypeMixin
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django_enum import EnumField
from django_enum.utils import values
import tests
from tests.djenum.models import (
    AdminDisplayBug35,
    EnumTester,
    NullBlankFormTester,
    NullableBlankFormTester,
    Bug53Tester,
    NullableStrFormTester,
    AltWidgetTester,
)
from tests.djenum.enums import (
    ExternEnum,
    NullableExternEnum,
    StrTestEnum,
    NullableStrEnum,
    GNSSConstellation,
    TextEnum,
)
from playwright.sync_api import sync_playwright, expect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.db.models.fields import NOT_PROVIDED
from django_enum.utils import decompose
from django.db import connection


class TestAdmin(EnumTypeMixin, LiveServerTestCase):
    BUG35_CLASS = AdminDisplayBug35

    def test_admin_list_display_bug35(self):
        from django.contrib.auth import get_user_model

        get_user_model().objects.create_superuser(
            username="admin",
            email="admin@django-enum.com",
            password="admin_password",
        )
        self.client.login(username="admin", password="admin_password")

        obj = self.BUG35_CLASS.objects.create()

        resp = self.client.get(
            reverse(
                f"admin:{self.BUG35_CLASS._meta.label_lower.replace('.', '_')}_changelist"
            )
        )
        self.assertContains(resp, '<td class="field-int_enum">Value 2</td>')
        change_link = reverse(
            f"admin:{self.BUG35_CLASS._meta.label_lower.replace('.', '_')}_change",
            args=[obj.id],
        )
        self.assertContains(resp, f'<a href="{change_link}">Value1</a>')

    def test_admin_change_display_bug35(self):
        from django.contrib.auth import get_user_model

        get_user_model().objects.create_superuser(
            username="admin",
            email="admin@django-enum.com",
            password="admin_password",
        )
        self.client.login(username="admin", password="admin_password")

        obj = self.BUG35_CLASS.objects.create()
        resp = self.client.get(
            reverse(
                f"admin:{self.BUG35_CLASS._meta.label_lower.replace('.', '_')}_change",
                args=[obj.id],
            )
        )
        self.assertContains(resp, '<div class="readonly">Value1</div>')
        self.assertContains(resp, '<div class="readonly">Value 2</div>')


class _GenericAdminFormTest(StaticLiveServerTestCase):
    MODEL_CLASS: t.Type[Model]

    HEADLESS = tests.HEADLESS

    __test__ = False

    use_radio = False
    use_checkbox = False

    pytestmark = pytest.mark.ui

    record_screenshots = False

    def enum(self, field: str) -> t.Type[Enum]:
        enum = t.cast(EnumField, self.MODEL_CLASS._meta.get_field(field)).enum
        assert enum
        return enum

    @property
    def changes(self) -> t.List[t.Dict[str, t.Any]]:
        # must implement
        return [{}]

    @property
    def add_url(self):
        path = reverse(
            f"admin:{self.MODEL_CLASS._meta.label_lower.replace('.', '_')}_add"
        )
        return f"{self.live_server_url}{path}"

    def change_url(self, id):
        path = reverse(
            f"admin:{self.MODEL_CLASS._meta.label_lower.replace('.', '_')}_change",
            args=[id],
        )
        return f"{self.live_server_url}{path}"

    @property
    def list_url(self):
        path = reverse(
            f"admin:{self.MODEL_CLASS._meta.label_lower.replace('.', '_')}_changelist"
        )
        return f"{self.live_server_url}{path}"

    def get_object_ids(self):
        self.page.goto(self.list_url)
        return self.page.eval_on_selector_all(
            "input[name='_selected_action']", "elements => elements.map(e => e.value)"
        )

    @classmethod
    def setUpClass(cls):
        """Set up the test class with a live server and Playwright instance."""
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "1"
        super().setUpClass()
        # cls.record_screenshots = pytest.Config.getoption("--record-screenshots")
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=cls.HEADLESS)
        cls.page = cls.browser.new_page()

    @classmethod
    def tearDownClass(cls):
        """Clean up Playwright instance after tests."""
        cls.page.close()
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()
        del os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"]

    def setUp(self):
        """Create an admin user before running tests."""
        self.admin_username = "admin"
        self.admin_password = "password"

        get_user_model().objects.create_superuser(
            username=self.admin_username, password=self.admin_password
        )

        # Log in to the Django admin
        self.page.goto(f"{self.live_server_url}/admin/login/")
        self.page.fill("input[name='username']", self.admin_username)
        self.page.fill("input[name='password']", self.admin_password)
        self.page.click("input[type='submit']")

        # Ensure login is successful
        expect(self.page).to_have_url(f"{self.live_server_url}/admin/")

    def set_form_value(
        self, field_name: str, value: t.Optional[t.Union[Enum, str]], flag=False
    ):
        # if field_name == "constellation_null" and value is None:
        #     import ipdb
        #     ipdb.set_trace()
        if value is None and None in values(self.enum(field_name)):
            value = self.enum(field_name)(value)
        # should override this if needed
        if getattr(value, "value", value) is None and not flag:
            if self.use_radio:
                self.page.click(f"input[name='{field_name}'][value='']")
            else:
                self.page.select_option(f"select[name='{field_name}']", "")
        elif flag:
            if self.use_checkbox:
                for checkbox in self.page.locator(
                    f"input[type='checkbox'][name='{field_name}']"
                ).all():
                    if checkbox.is_checked():
                        checkbox.uncheck()
                if value is not None:
                    assert isinstance(value, Flag)
                    for flag in decompose(value):
                        self.page.check(
                            f"input[name='{field_name}'][value='{flag.value}']"
                        )
            else:
                if value is not None:
                    assert isinstance(value, Flag)
                    self.page.select_option(
                        f"select[name='{field_name}']",
                        [str(flag.value) for flag in decompose(value)],
                    )
                else:
                    self.page.select_option(f"select[name='{field_name}']", [])
        else:
            if self.use_radio:
                self.page.click(
                    f"input[name='{field_name}'][value='{getattr(value, 'value', value)}']"
                )
            else:
                self.page.select_option(
                    f"select[name='{field_name}']",
                    str(getattr(value, "value", value)),
                )

    def verify_changes(self, obj: Model, expected: t.Dict[str, t.Any]):
        count = 0
        for field in obj._meta.get_fields():
            if field.name == "id":
                continue
            if field.name not in expected:
                continue
            if not isinstance(field, EnumField):
                continue
            count += 1
            obj_val = getattr(obj, field.name)
            exp = expected[field.name]
            if not field.coerce:
                exp = getattr(exp, "value", exp)
            if exp is None or (isinstance(exp, str) and not exp):
                if isinstance(obj_val, Flag) and connection.vendor == "oracle":
                    self.assertEqual(obj_val, self.enum(field.name)(0))
                elif isinstance(obj_val, Enum):
                    self.assertIsNone(
                        obj_val.value, f"{obj._meta.model_name}.{field.name}"
                    )
                elif isinstance(obj_val, str):
                    self.assertEqual(
                        obj_val, exp, f"{obj._meta.model_name}.{field.name}"
                    )
                else:
                    try:
                        self.assertIsNone(
                            obj_val, f"{obj._meta.model_name}.{field.name}"
                        )
                    except AssertionError:
                        if connection.vendor == "oracle" and issubclass(
                            self.enum(field.name), Flag
                        ):
                            # TODO - why is oracle returning 0 instead of None?
                            self.assertEqual(obj_val, self.enum(field.name)(0))
                        else:
                            raise
            else:
                self.assertEqual(obj_val, exp, f"{obj._meta.model_name}.{field.name}")

        # sanity check
        self.assertEqual(count, len(expected))

    def do_add(self) -> Model:
        obj_ids = set(self.get_object_ids())

        self.page.goto(self.add_url)

        for field, value in self.changes[0].items():
            self.set_form_value(
                field,
                value,
                flag=issubclass(self.MODEL_CLASS._meta.get_field(field).enum, Flag),
            )

        # create with all default fields
        with self.page.expect_navigation() as nav_info:
            self.page.click("input[name='_save']")

        response = nav_info.value
        assert response.status < 400

        # verify the add
        added_obj = self.MODEL_CLASS.objects.get(
            id=list(set(self.get_object_ids()) - obj_ids)[0]
        )

        defaults = {}

        for field in added_obj._meta.get_fields():
            if field.name == "id" or not isinstance(field, EnumField):
                continue
            enum = getattr(field, "enum", None)
            expected = field.default
            if field.default is NOT_PROVIDED:
                expected = None
                if enum and issubclass(enum, Flag) and not field.null:
                    expected = enum(0)
            defaults[field.name] = expected

        self.verify_changes(added_obj, {**defaults, **self.changes[0]})
        return added_obj

    def do_change(self, obj: Model):
        # test change forms
        for changes in self.changes[1:]:
            # go to the change page
            self.page.goto(self.change_url(obj.pk))

            # make form selections
            for field, value in changes.items():
                self.set_form_value(
                    field,
                    value,
                    flag=issubclass(self.MODEL_CLASS._meta.get_field(field).enum, Flag),
                )

            # save
            with self.page.expect_navigation():
                self.page.click("input[name='_save']")

            obj.refresh_from_db()
            self.verify_changes(obj, changes)

    def do_delete(self, obj: Model):
        # delete the object
        self.page.goto(self.change_url(obj.pk))
        self.page.click("a.deletelink")
        with self.page.expect_navigation():
            self.page.click("input[type='submit']")

        # verify deletion
        self.assertFalse(self.MODEL_CLASS.objects.filter(pk=obj.pk).exists())

    def test_admin_form_add_change_delete(self):
        """Tests add, change, and delete operations in Django Admin."""

        obj = self.do_add()
        self.do_change(obj)
        self.do_delete(obj)


class TestEnumTesterAdminForm(EnumTypeMixin, _GenericAdminFormTest):
    MODEL_CLASS = EnumTester
    __test__ = True

    @property
    def changes(self) -> t.List[t.Dict[str, t.Any]]:
        return [
            {},
            {
                "small_pos_int": self.SmallPosIntEnum.VAL2,
                "small_int": self.SmallIntEnum.VAL0,
                "pos_int": self.PosIntEnum.VAL1,
                "int": self.IntEnum.VALn1,
                "big_pos_int": self.BigPosIntEnum.VAL2,
                "big_int": self.BigIntEnum.VAL2,
                "constant": self.Constants.GOLDEN_RATIO,
                "text": self.TextEnum.VALUE2,
                "extern": self.ExternEnum.TWO,
                "date_enum": self.DateEnum.EMMA,
                "datetime_enum": self.DateTimeEnum.ST_HELENS,
                "duration_enum": self.DurationEnum.DAY,
                "time_enum": self.TimeEnum.MORNING,
                "decimal_enum": self.DecimalEnum.ONE,
                "dj_int_enum": self.DJIntEnum.TWO,
                "dj_text_enum": self.DJTextEnum.C,
                "non_strict_int": self.SmallPosIntEnum.VAL1,
                "non_strict_text": self.TextEnum.VALUE3,
                "no_coerce": self.SmallPosIntEnum.VAL3,
            },
        ]


class TestNullBlankAdminBehavior(_GenericAdminFormTest):
    MODEL_CLASS = NullBlankFormTester
    __test__ = True

    @property
    def changes(self) -> t.List[t.Dict[str, t.Any]]:
        return [
            {"required": ExternEnum.THREE, "blank": ExternEnum.TWO},
            {
                "required": ExternEnum.ONE,
                "required_default": ExternEnum.THREE,
                "blank": ExternEnum.ONE,
                "blank_nullable": None,
                "blank_nullable_default": None,
            },
            {
                "required": ExternEnum.ONE,
                "required_default": ExternEnum.THREE,
                "blank": ExternEnum.ONE,
                "blank_nullable": ExternEnum.ONE,
                "blank_nullable_default": ExternEnum.TWO,
            },
            {
                "required": ExternEnum.ONE,
                "required_default": ExternEnum.THREE,
                "blank": ExternEnum.ONE,
                "blank_nullable": "",
                "blank_nullable_default": "",
            },
        ]


@pytest.mark.skipif(
    connection.vendor == "oracle", reason="Null/blank form behavior on oracle broken"
)
class TestNullableBlankAdminBehavior(_GenericAdminFormTest):
    MODEL_CLASS = NullableBlankFormTester
    __test__ = True
    HEADLESS = tests.HEADLESS

    @property
    def changes(self) -> t.List[t.Dict[str, t.Any]]:
        return [
            {"required": NullableExternEnum.THREE, "blank": NullableExternEnum.TWO},
            {
                "required": NullableExternEnum.ONE,
                "required_default": NullableExternEnum.THREE,
                "blank": NullableExternEnum.ONE,
                "blank_nullable": None,
                "blank_nullable_default": None,
            },
            {
                "required": NullableExternEnum.ONE,
                "required_default": NullableExternEnum.THREE,
                "blank": NullableExternEnum.ONE,
                "blank_nullable": NullableExternEnum.ONE,
                "blank_nullable_default": NullableExternEnum.TWO,
            },
            {
                "required": NullableExternEnum.ONE,
                "required_default": NullableExternEnum.THREE,
                "blank": NullableExternEnum.ONE,
                "blank_nullable": "",
                "blank_nullable_default": "",
            },
        ]


@pytest.mark.skipif(
    connection.vendor == "oracle", reason="Null/blank form behavior on oracle broken"
)
class TestNullableStrAdminBehavior(_GenericAdminFormTest):
    MODEL_CLASS = NullableStrFormTester
    __test__ = True
    HEADLESS = tests.HEADLESS

    @property
    def changes(self) -> t.List[t.Dict[str, t.Any]]:
        return [
            {"required": NullableStrEnum.STR1, "blank": NullableStrEnum.STR2},
            {
                "required": NullableStrEnum.STR2,
                "required_default": NullableStrEnum.STR1,
                "blank": NullableStrEnum.STR2,
                "blank_nullable": None,
                "blank_nullable_default": None,
            },
            {
                "required": NullableStrEnum.STR1,
                "required_default": NullableStrEnum.STR2,
                "blank": NullableStrEnum.STR2,
                "blank_nullable": NullableStrEnum.STR1,
                "blank_nullable_default": NullableStrEnum.NONE,
            },
            {
                "required": NullableStrEnum.STR2,
                "required_default": NullableStrEnum.STR2,
                "blank": NullableStrEnum.STR1,
                "blank_nullable": "",
                "blank_nullable_default": "",
            },
        ]


class TestBug53AdminBehavior(_GenericAdminFormTest):
    MODEL_CLASS = Bug53Tester
    __test__ = True

    @property
    def changes(self) -> t.List[t.Dict[str, t.Any]]:
        return [
            {
                "char_blank_null_false": StrTestEnum.V2,
                "int_blank_null_false": ExternEnum.TWO,
            },
        ]

    def test_500_error(self):
        # when null=False and blank=True on an enum field that has an enum that
        # does not accept the blank value "" a value error will be allowed to propagate out
        # of the form.save(). This is expected and on the user of the library to address. It
        # happens because "" is fine given the form logic definiton but is not given the database
        # requirements. Nothing to do about it.

        self.page.goto(self.add_url)

        # make form selections
        for field, value in {"char_blank_null_false": StrTestEnum.V2}.items():
            self.set_form_value(field, value)

        # save
        with self.page.expect_response(lambda response: response.status == 500):
            self.page.click("input[name='_save']")


class TestAltWidgetAdminForm(_GenericAdminFormTest):
    MODEL_CLASS = AltWidgetTester
    __test__ = True
    HEADLESS = tests.HEADLESS

    use_radio = True
    use_checkbox = True

    @property
    def changes(self) -> t.List[t.Dict[str, t.Any]]:
        return [
            {
                "text": TextEnum.VALUE1,
                "constellation": GNSSConstellation.BEIDOU | GNSSConstellation.GPS,
                "constellation_non_strict": (
                    GNSSConstellation.BEIDOU | GNSSConstellation.QZSS
                ),
            },
            {
                "text": TextEnum.VALUE2,
                "text_null": TextEnum.VALUE2,
                "constellation": GNSSConstellation(0),
                "constellation_null": GNSSConstellation.GLONASS | GNSSConstellation.GPS,
                "constellation_non_strict": (GNSSConstellation(0)),
            },
            {
                "text": TextEnum.DEFAULT,
                "text_null": None,
                "constellation": GNSSConstellation.GALILEO,
                "constellation_null": None,
                "constellation_non_strict": (GNSSConstellation.GALILEO),
            },
        ]

    def test_non_strict_radio_and_checkbox(self):
        obj = AltWidgetTester.objects.create(
            text_non_strict="A" * 10,
            constellation_non_strict=(
                GNSSConstellation.BEIDOU | GNSSConstellation.QZSS | 1 << 7
            ),
        )

        self.page.goto(self.change_url(obj.pk))

        def verify_labels(inputs, expected):
            # there is a bug in django 3.2 where the group label uses the id of the first
            # label which means this verification breaks. Since 3.2 is already out we
            # just elide the check < 4.2
            if django.VERSION[:2] < (4, 2):
                return
            for i in range(inputs.count()):
                radio = inputs.nth(i)
                rid = radio.get_attribute("id")
                label = (
                    self.page.locator(f"label[for='{rid}']").first.inner_text().strip()
                )
                self.assertTrue(label in expected, f"{label} not in {expected}")
                expected.remove(label)

        # text
        checked_text = self.page.locator("input[type='radio'][name='text']:checked")
        self.assertEqual(checked_text.count(), 1)
        self.assertEqual(
            checked_text.first.get_attribute("value"),
            str(AltWidgetTester._meta.get_field("text").default.value),
        )
        text_radios = self.page.locator("input[type='radio'][name='text']")
        self.assertEqual(text_radios.count(), len(TextEnum))
        verify_labels(text_radios, [en.label for en in TextEnum])

        # text_null
        checked_text_null = self.page.locator(
            "input[type='radio'][name='text_null']:checked"
        )
        self.assertEqual(checked_text_null.count(), 1)
        self.assertEqual(checked_text_null.first.get_attribute("value"), "")
        text_null_radios = self.page.locator("input[type='radio'][name='text_null']")
        self.assertEqual(text_null_radios.count(), len(TextEnum) + 1)
        verify_labels(
            text_null_radios, [BLANK_CHOICE_DASH[0][1]] + [en.label for en in TextEnum]
        )

        # text_non_strict
        checked_text_non_strict = self.page.locator(
            "input[type='radio'][name='text_non_strict']:checked"
        )
        self.assertEqual(checked_text_non_strict.count(), 1)
        self.assertEqual(checked_text_non_strict.first.get_attribute("value"), "A" * 10)
        text_non_strict_radios = self.page.locator(
            "input[type='radio'][name='text_non_strict']"
        )
        self.assertEqual(text_non_strict_radios.count(), len(TextEnum) + 1)
        verify_labels(
            text_non_strict_radios, [en.label for en in TextEnum] + ["A" * 10]
        )

        # constellation
        constellation_checkboxes = self.page.locator(
            "input[type='checkbox'][name='constellation']"
        )
        self.assertEqual(constellation_checkboxes.count(), 5)
        constellation_checked = self.page.locator(
            "input[type='checkbox'][name='constellation']:checked"
        )
        self.assertEqual(constellation_checked.count(), 0)
        verify_labels(constellation_checkboxes, [en.name for en in GNSSConstellation])

        # constellation_null
        constellation_null_checkboxes = self.page.locator(
            "input[type='checkbox'][name='constellation_null']"
        )
        self.assertEqual(constellation_null_checkboxes.count(), 5)
        constellation_null_checked = self.page.locator(
            "input[type='checkbox'][name='constellation_null']:checked"
        )
        self.assertEqual(constellation_null_checked.count(), 0)
        verify_labels(
            constellation_null_checkboxes, [en.name for en in GNSSConstellation]
        )

        # constellation_non_strict
        constellation_non_strict_checkboxes = self.page.locator(
            "input[type='checkbox'][name='constellation_non_strict']"
        )
        self.assertEqual(constellation_non_strict_checkboxes.count(), 6)
        constellation_non_strict_checked = self.page.locator(
            "input[type='checkbox'][name='constellation_non_strict']:checked"
        )
        self.assertEqual(constellation_non_strict_checked.count(), 3)
        verify_labels(
            constellation_non_strict_checkboxes,
            [en.name for en in GNSSConstellation] + ["7"],
        )
        for i in range(constellation_non_strict_checked.count()):
            checkbox = constellation_non_strict_checked.nth(i)
            value = checkbox.get_attribute("value")
            self.assertTrue(
                value
                in [
                    str(GNSSConstellation.BEIDOU.value),
                    str(GNSSConstellation.QZSS.value),
                    "128",
                ]
            )
