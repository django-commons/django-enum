"""
The models as they were defined against django-enum 2.x. These are only used
to generate ``migrations/0001_initial.py`` (see ``just make-legacy-migrations``)
and must not be imported by the test suite.

The enumerations use the 2.x technique of naming the sign bit with a negative
value so that it fits in a signed 32 or 64 bit column.
"""

from enum import IntFlag

from django.db import models

from tests.legacy_migrations.fields import (
    SignedBigIntegerFlagField,
    SignedIntegerFlagField,
)


class Permissions32(IntFlag):
    READ = 1 << 0
    WRITE = 1 << 1
    EXECUTE = 1 << 2
    ADMIN = -1 << 31


class Permissions64(IntFlag):
    READ = 1 << 0
    WRITE = 1 << 1
    EXECUTE = 1 << 2
    ADMIN = -1 << 63


class LegacyFlagModel(models.Model):
    permissions = SignedIntegerFlagField(Permissions32)
    big_permissions = SignedBigIntegerFlagField(Permissions64)
    nullable = SignedIntegerFlagField(Permissions32, null=True, default=None)
