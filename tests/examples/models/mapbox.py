# flake8: noqa
import typing as t
from django.db import models
from enum_properties import symmetric, Symmetric, IntEnumProperties
from django_enum import EnumField


class Map(models.Model):

    class MapBoxStyle(IntEnumProperties):
        """
        https://docs.mapbox.com/api/maps/styles/
        """

        label: t.Annotated[str, Symmetric(case_fold=True)]
        slug: t.Annotated[str, Symmetric(case_fold=True)]
        version: int

        # fmt: off
        # name            value  label                slug          version
        STREETS           = 1, "Streets",           "streets",           12
        OUTDOORS          = 2, "Outdoors",          "outdoors",          12
        LIGHT             = 3, "Light",             "light",             11
        DARK              = 4, "Dark",              "dark",              11
        SATELLITE         = 5, "Satellite",         "satellite",          9
        SATELLITE_STREETS = 6, "Satellite Streets", "satellite-streets", 12
        NAVIGATION_DAY    = 7, "Navigation Day",    "navigation-day",     1
        NAVIGATION_NIGHT  = 8, "Navigation Night",  "navigation-night",   1
        # fmt: on

        @symmetric()  # type: ignore[prop-decorator]
        @property
        def uri(self):
            return f"mapbox://styles/mapbox/{self.slug}-v{self.version}"

        def __str__(self):
            return self.uri

    style = EnumField(MapBoxStyle, default=MapBoxStyle.STREETS)
