"""
The models from :mod:`tests.legacy_migrations.v2.models` as they should be
written for django-enum 3.x: the sign bit is spelled ``1 << 31`` /
``1 << 63`` and the stock flag fields are used. ``migrations/0002`` is the
migration generated for this change and the tests verify that data written by
django-enum 2.x is read back correctly after it is applied.
"""

from enum import IntFlag

from django.db import models

from django_enum import EnumField


class Permissions32(IntFlag):
    READ = 1 << 0
    WRITE = 1 << 1
    EXECUTE = 1 << 2
    ADMIN = 1 << 31


class Permissions64(IntFlag):
    READ = 1 << 0
    WRITE = 1 << 1
    EXECUTE = 1 << 2
    ADMIN = 1 << 63


class LegacyFlagModel(models.Model):
    permissions = EnumField(Permissions32)
    big_permissions = EnumField(Permissions64)
    nullable = EnumField(Permissions32, null=True, default=None)
