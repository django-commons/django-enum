"""
The CheckConstraint check variable was renamed to condition in Django 6.0, so we need
to maintain compatibility with both versions in our migrations.
"""

import django
from django.db import models


if django.VERSION < (5, 0):

    def CheckConstraint(*args, **kwargs):
        return models.CheckConstraint(
            *args, check=kwargs.pop("condition", None), **kwargs
        )
else:
    CheckConstraint = models.CheckConstraint
