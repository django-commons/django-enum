from django.apps import AppConfig


class LegacyMigrationsConfig(AppConfig):
    name = "tests.legacy_migrations"
    label = name.replace(".", "_")
