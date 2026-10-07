"""
Minimal settings used only to generate the frozen legacy migration with an
old release of django-enum. See ``just make-legacy-migrations``.
"""

SECRET_KEY = "legacy"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
INSTALLED_APPS = ["tests.legacy_migrations.v2"]
MIGRATION_MODULES = {"tests_legacy_migrations": "tests.legacy_migrations.migrations"}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = False
