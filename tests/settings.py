import os
import sys
import typing as t
from pathlib import Path

from django import VERSION as django_version

try:
    import django_stubs_ext

    django_stubs_ext.monkeypatch()
except ImportError:
    pass

DEBUG = not os.environ.get("IS_PYTEST_RUN", False)
SECRET_KEY = "psst"
SITE_ID = 1
USE_TZ = False

rdbms = os.environ.get("RDBMS", "sqlite")

if rdbms == "sqlite":  # pragma: no cover
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "test.db",
            "USER": "",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "",
        }
    }
elif rdbms == "postgres":  # pragma: no cover
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "postgres"),
            "USER": os.environ.get("POSTGRES_USER", "postgres"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", ""),
            "PORT": os.environ.get("POSTGRES_PORT", ""),
        }
    }
elif rdbms == "mysql":  # pragma: no cover
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("MYSQL_DATABASE", "test"),
            "USER": os.environ.get("MYSQL_USER", "root"),
            "PASSWORD": os.environ.get("MYSQL_PASSWORD", "root"),
            "HOST": os.environ.get("MYSQL_HOST", "127.0.0.1"),
            "PORT": os.environ.get("MYSQL_PORT", "3306"),
        }
    }
elif rdbms == "mariadb":  # pragma: no cover
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("MARIADB_DATABASE", "test"),
            "USER": os.environ.get("MARIADB_USER", "root"),
            "PASSWORD": os.environ.get("MARIADB_PASSWORD", "root"),
            "HOST": os.environ.get("MARIADB_HOST", "127.0.0.1"),
            "PORT": os.environ.get("MARIADB_PORT", "3306"),
        }
    }
elif rdbms == "oracle":  # pragma: no cover
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.oracle",
            "NAME": f"{os.environ.get('ORACLE_HOST', 'localhost')}:"
            f"{os.environ.get('ORACLE_PORT', '1521')}"
            f"/{os.environ.get('ORACLE_DATABASE', 'XEPDB1')}",
            "USER": os.environ.get("ORACLE_USER", "system"),
            "PASSWORD": os.environ.get("ORACLE_PASSWORD", "password"),
        }
    }
    try:
        import oracledb

        oracledb.init_oracle_client()
    except ImportError:
        pass

# from django.db.backends.oracle.base import FormatStylePlaceholderCursor
# from django.db.backends import utils
# from django.db.backends.base import schema
# from django.db.models.constraints import CheckConstraint
# from django.db.backends.oracle.schema import DatabaseSchemaEditor
# from django.db.backends.postgresql.schema import DatabaseSchemaEditor
# from django.db.backends.mysql.schema import DatabaseSchemaEditor

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

INSTALLED_APPS = [
    "tests.benchmark",
    *(["tests.flag_constraints"] if sys.version_info >= (3, 11) else []),
    "tests.constraints",
    "tests.converters",
    "tests.djenum",
    "tests.tmpls",
    # "debug_toolbar",
    # "django_extensions",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
]
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

if django_version[0:2] >= (5, 0):  # pragma: no cover
    INSTALLED_APPS.insert(0, "tests.db_default")

try:
    import rest_framework

    INSTALLED_APPS.insert(0, "rest_framework")
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass

try:
    import enum_properties

    INSTALLED_APPS.insert(0, "tests.enum_prop")
    INSTALLED_APPS.insert(0, "tests.edit_tests")
    INSTALLED_APPS.insert(0, "tests.examples")
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    pass

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

STATIC_ROOT = Path(__file__).parent / "global_static"
STATIC_URL = "/static/"

DEBUG = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEST_EDIT_DIR = Path(__file__).parent / "edit_tests" / "edits"
TEST_MIGRATION_DIR = Path(__file__).parent / "edit_tests" / "migrations"

REST_FRAMEWORK: t.Dict[str, t.Any] = {
    # no auth
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}
