from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from tests.djenum import views
from tests.enum_prop import enums as prop_enums
from tests.enum_prop.enums import (
    BigIntEnum,
    BigPosIntEnum,
    Constants,
    DJIntEnum,
    DJTextEnum,
    ExternEnum,
    IntEnum,
    PosIntEnum,
    SmallIntEnum,
    SmallPosIntEnum,
    TextEnum,
    DateEnum,
    DateTimeEnum,
    TimeEnum,
    DurationEnum,
    DecimalEnum,
)
from tests.enum_prop.forms import EnumTesterForm
from tests.enum_prop.models import EnumTester


class EnumTesterDetailView(views.EnumTesterDetailView):
    model = EnumTester
    NAMESPACE = "tests_enum_prop"
    enums = prop_enums


class EnumTesterListView(views.EnumTesterListView):
    model = EnumTester
    NAMESPACE = "tests_enum_prop"
    enums = prop_enums


class EnumTesterCreateView(views.URLMixin, CreateView):
    model = EnumTester
    template_name = "enumtester_form.html"
    NAMESPACE = "tests_enum_prop"
    enums = prop_enums
    form_class = EnumTesterForm


class EnumTesterUpdateView(views.URLMixin, UpdateView):
    model = EnumTester
    template_name = "enumtester_form.html"
    NAMESPACE = "tests_enum_prop"
    enums = prop_enums
    form_class = EnumTesterForm

    def get_success_url(self):  # pragma: no cover
        return reverse(f"{self.NAMESPACE}:enum-update", kwargs={"pk": self.object.pk})


class EnumTesterDeleteView(views.URLMixin, DeleteView):
    NAMESPACE = "tests_enum_prop"
    model = EnumTester
    template_name = "enumtester_form.html"
    enums = prop_enums
    form_class = EnumTesterForm

    def get_success_url(self):  # pragma: no cover
        return reverse(f"{self.NAMESPACE}:enum-list")


try:
    from rest_framework import serializers, viewsets

    from django_enum.drf import EnumFieldMixin

    class EnumTesterSerializer(EnumFieldMixin, serializers.ModelSerializer):
        class Meta:
            model = EnumTester
            fields = "__all__"

    class DRFView(viewsets.ModelViewSet):
        queryset = EnumTester.objects.all()
        serializer_class = EnumTesterSerializer

except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass

try:
    from django_filters.views import FilterView
    from tests.djenum.views import EnumTesterFilterViewSet
    from django_enum.filters import FilterSet as EnumFilterSet, MultipleEnumFilter

    class EnumTesterPropFilterViewSet(EnumTesterFilterViewSet):
        enums = prop_enums

        class EnumTesterPropFilter(EnumFilterSet):
            class Meta:
                model = EnumTester
                fields = "__all__"

        filterset_class = EnumTesterPropFilter
        model = EnumTester

    class EnumTesterPropMultipleFilterViewSet(views.URLMixin, FilterView):
        class EnumTesterMultipleFilter(EnumFilterSet):
            small_pos_int = MultipleEnumFilter(enum=SmallPosIntEnum)
            small_int = MultipleEnumFilter(enum=SmallIntEnum)
            pos_int = MultipleEnumFilter(enum=PosIntEnum)
            int = MultipleEnumFilter(enum=IntEnum)
            big_pos_int = MultipleEnumFilter(enum=BigPosIntEnum)
            big_int = MultipleEnumFilter(enum=BigIntEnum)
            constant = MultipleEnumFilter(enum=Constants)
            text = MultipleEnumFilter(enum=TextEnum)
            extern = MultipleEnumFilter(enum=ExternEnum)

            dj_int_enum = MultipleEnumFilter(enum=DJIntEnum)
            dj_text_enum = MultipleEnumFilter(enum=DJTextEnum)

            # Non-strict
            non_strict_int = MultipleEnumFilter(enum=SmallPosIntEnum, strict=False)
            non_strict_text = MultipleEnumFilter(enum=TextEnum, strict=False)
            no_coerce = MultipleEnumFilter(enum=SmallPosIntEnum, strict=False)

            # eccentric enums
            date_enum = MultipleEnumFilter(enum=DateEnum)
            datetime_enum = MultipleEnumFilter(enum=DateTimeEnum)
            time_enum = MultipleEnumFilter(enum=TimeEnum)
            duration_enum = MultipleEnumFilter(enum=DurationEnum)
            decimal_enum = MultipleEnumFilter(enum=DecimalEnum)

            class Meta:
                fields = [
                    "small_pos_int",
                    "small_int",
                    "pos_int",
                    "int",
                    "big_pos_int",
                    "big_int",
                    "constant",
                    "text",
                    "extern",
                    "non_strict_int",
                    "non_strict_text",
                    "no_coerce",
                    "date_enum",
                    "datetime_enum",
                    "time_enum",
                    "duration_enum",
                    "decimal_enum",
                ]
                model = EnumTester

        filterset_class = EnumTesterMultipleFilter
        model = EnumTester
        template_name = "enumtester_list.html"

except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass
