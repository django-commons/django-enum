from django.contrib import admin

from django.forms import ModelForm, RadioSelect
from django_enum.forms import (
    NonStrictRadioSelect,
    FlagCheckbox,
    NonStrictFlagCheckbox,
)
from django_enum.utils import decompose

from tests.djenum.enums import TextEnum, GNSSConstellation
from tests.djenum.models import (
    AdminDisplayBug35,
    EnumTester,
    NullBlankFormTester,
    NullableBlankFormTester,
    Bug53Tester,
    NullableStrFormTester,
    AltWidgetTester,
)

admin.site.register(EnumTester)
admin.site.register(NullBlankFormTester)
admin.site.register(NullableBlankFormTester)
admin.site.register(Bug53Tester)
admin.site.register(NullableStrFormTester)


class AdminDisplayBug35Admin(admin.ModelAdmin):
    list_display = (
        "text_enum",
        "int_enum",
        "status_basic",
        "status_basic_int",
        "status_str",
        "status_int",
    )
    readonly_fields = ("text_enum", "int_enum", "blank_int", "blank_txt")


admin.site.register(AdminDisplayBug35, AdminDisplayBug35Admin)


class AltWidgetAdminForm(ModelForm):
    class Meta:
        model = AltWidgetTester
        fields = "__all__"
        widgets = {
            "text": RadioSelect,
            "text_null": RadioSelect,
            "text_non_strict": NonStrictRadioSelect,
            "constellation": FlagCheckbox,
            "constellation_null": FlagCheckbox,
            "constellation_non_strict": NonStrictFlagCheckbox,
        }


class AltWidgetAdmin(admin.ModelAdmin):
    form = AltWidgetAdminForm
    list_display = (
        "text",
        "text_null",
        "text_non_strict",
        "constellations",
        "constellations_null",
        "constellations_non_strict",
    )

    def constellations(self, obj):
        return ", ".join([str(c.name) for c in decompose(obj.constellation)])

    def constellations_null(self, obj):
        if obj.constellation_null is None:
            return "None"
        return ", ".join([str(c.name) for c in decompose(obj.constellation_null)])

    def constellations_non_strict(self, obj):
        return ", ".join([str(c.name) for c in decompose(obj.constellation_non_strict)])


admin.site.register(AltWidgetTester, AltWidgetAdmin)
