from django.apps import AppConfig


class LegacyMigrationsV2Config(AppConfig):
    """
    Same app label as :mod:`tests.legacy_migrations` so that the migration
    generated from these models lands in that app's history.
    """

    name = "tests.legacy_migrations.v2"
    label = "tests_legacy_migrations"
