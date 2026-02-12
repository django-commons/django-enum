from django.contrib import admin
from django.forms import ModelForm, Select, RadioSelect
from django_enum.forms import (
    NonStrictRadioSelect,
    FlagSelectMultiple,
    FlagCheckbox,
    NonStrictFlagCheckbox,
    NonStrictFlagSelectMultiple,
    NonStrictSelect
)
from tests.examples.models import (
    Map,
    BasicExample,
    FlagExample,
    NoCoerceExample,
    StrictExample,
    PropertyExample,
    ChoicesWithProperties,
    TextChoicesExample,
    WidgetDemoStrict,
    WidgetDemoNonStrict,
    WidgetDemoRadiosAndChecks,
    WidgetDemoRadiosAndChecksNonStrict,
    WidgetDemoRadiosAndChecksNulls
)

admin.site.register(Map)
admin.site.register(StrictExample)
admin.site.register(NoCoerceExample)
admin.site.register(PropertyExample)
admin.site.register(BasicExample)
admin.site.register(FlagExample)
admin.site.register(ChoicesWithProperties)
admin.site.register(TextChoicesExample)


class WidgetDemoStrictAdminForm(ModelForm):
    class Meta:
        model = WidgetDemoStrict
        fields = "__all__"
        widgets = {
            "color": Select,
            "permissions": FlagSelectMultiple,
        }


class WidgetDemoStrictAdmin(admin.ModelAdmin):
    form = WidgetDemoStrictAdminForm


admin.site.register(WidgetDemoStrict, WidgetDemoStrictAdmin)


class WidgetDemoNonStrictAdminForm(ModelForm):
    class Meta:
        model = WidgetDemoNonStrict
        fields = "__all__"
        widgets = {
            "color": NonStrictSelect,
            "permissions": NonStrictFlagSelectMultiple,
        }


class WidgetDemoNonStrictAdmin(admin.ModelAdmin):
    form = WidgetDemoNonStrictAdminForm



admin.site.register(WidgetDemoNonStrict, WidgetDemoNonStrictAdmin)


class WidgetDemoRadiosAndChecksAdminForm(ModelForm):
    class Meta:
        model = WidgetDemoRadiosAndChecks
        fields = "__all__"
        widgets = {
            "color": RadioSelect,
            "permissions": FlagCheckbox,
        }


class WidgetDemoRadiosAndChecksAdmin(admin.ModelAdmin):
    form = WidgetDemoRadiosAndChecksAdminForm


class WidgetDemoRadiosAndChecksNullsAdmin(admin.ModelAdmin):
    form = WidgetDemoRadiosAndChecksAdminForm


admin.site.register(WidgetDemoRadiosAndChecks, WidgetDemoRadiosAndChecksAdmin)
admin.site.register(WidgetDemoRadiosAndChecksNulls, WidgetDemoRadiosAndChecksNullsAdmin)


class WidgetDemoRadiosAndChecksNonStrictAdminForm(ModelForm):
    class Meta:
        model = WidgetDemoRadiosAndChecksNonStrict
        fields = "__all__"
        widgets = {
            "color": NonStrictRadioSelect,
            "permissions": NonStrictFlagCheckbox,
        }


class WidgetDemoRadiosAndChecksNonStrictAdmin(admin.ModelAdmin):
    form = WidgetDemoRadiosAndChecksNonStrictAdminForm


admin.site.register(WidgetDemoRadiosAndChecksNonStrict, WidgetDemoRadiosAndChecksNonStrictAdmin)
