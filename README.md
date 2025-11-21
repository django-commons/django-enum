# django-enum

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://docs.astral.sh/ruff)
[![PyPI version](https://badge.fury.io/py/django-enum.svg)](https://pypi.python.org/pypi/django-enum/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/django-enum.svg)](https://pypi.python.org/pypi/django-enum/)
[![PyPI djversions](https://img.shields.io/pypi/djversions/django-enum.svg)](https://pypi.org/project/django-enum/)
[![PyPI status](https://img.shields.io/pypi/status/django-enum.svg)](https://pypi.python.org/pypi/django-enum)
[![Documentation Status](https://readthedocs.org/projects/django-enum/badge/?version=latest)](http://django-enum.readthedocs.io/?badge=latest/)
[![Code Cov](https://codecov.io/gh/django-commons/django-enum/branch/main/graph/badge.svg?token=0IZOKN2DYL)](https://codecov.io/gh/django-commons/django-enum)
[![Test Status](https://github.com/django-commons/django-enum/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/django-commons/django-enum/actions/workflows/test.yml?query=branch:main)
[![Lint Status](https://github.com/django-commons/django-enum/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/django-commons/django-enum/actions/workflows/lint.yml?query=branch:main)
[![Published on Django Packages](https://img.shields.io/badge/Published%20on-Django%20Packages-0c3c26)](https://djangopackages.org/packages/p/django-enum/)

---------------------------------------------------------------------------------------------------

[![Postgres](https://img.shields.io/badge/Postgres-12%2B-blue)](https://www.postgresql.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-blue)](https://www.mysql.com/)
[![MariaDB](https://img.shields.io/badge/MariaDB-10.4%2B-blue)](https://mariadb.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.8%2B-blue)](https://www.sqlite.org/)
[![Oracle](https://img.shields.io/badge/Oracle-21c%2B-blue)](https://www.oracle.com/database/)

---------------------------------------------------------------------------------------------------

🚨 **See [migration guide](https://django-enum.readthedocs.io/en/latest/changelog.html#migration-1-x-to-2-x) for notes on 1.x to 2.x migration.** 🚨

Full and natural support for [PEP435](https://peps.python.org/pep-0435) [enumerations](https://docs.python.org/3/library/enum.html#enum.Enum) as [Django](https://www.djangoproject.com) model fields.

Many packages aim to ease usage of Python enumerations as model fields. Most were superseded when Django provided [TextChoices](https://docs.djangoproject.com/en/stable/ref/models/fields/#field-choices-enum-types) and [IntegerChoices](https://docs.djangoproject.com/en/stable/ref/models/fields/#field-choices-enum-types) types. The motivation for [django-enum](https://pypi.org/project/enum-properties) was to:

* Work with any [Enum](https://docs.python.org/3/library/enum.html#enum.Enum) including those that do not derive from Django's [TextChoices](https://docs.djangoproject.com/en/stable/ref/models/fields/#field-choices-enum-types) and [IntegerChoices](https://docs.djangoproject.com/en/stable/ref/models/fields/#field-choices-enum-types).
* Coerce fields to instances of the [Enum](https://docs.python.org/3/library/enum.html#enum.Enum) type by default.
* Allow strict adherence to [Enum](https://docs.python.org/3/library/enum.html#enum.Enum) values to be disabled.
* Handle migrations appropriately. (See [migrations](https://django-enum.readthedocs.io/en/latest/usage.html#migrations))
* Integrate as fully as possible with Django's [existing level of enum support](https://docs.djangoproject.com/en/stable/ref/models/fields/#field-choices-enum-types).
* Support [enum-properties](https://pypi.org/project/enum-properties) to enable richer enumeration types. (A less awkward alternative to [dataclass enumerations](https://docs.python.org/3/howto/enum.html#enum-dataclass-support) with more features)
* Represent enum fields with the smallest possible column type.
* Support [bit field](https://en.wikipedia.org/wiki/Bit_field) queries using standard Python Flag enumerations.
* Be as simple and light-weight an extension to core [Django](https://www.djangoproject.com) as possible.
* Enforce enumeration value consistency at the database level using [check constraints](https://docs.djangoproject.com/en/stable/ref/models/constraints) by default.
* (TODO) Support native database enumeration column types when available.

[django-enum](https://pypi.org/project/enum-properties) provides a new model field type, [EnumField](https://django-enum.rtfd.io/en/stable/reference/fields.html#django_enum.fields.EnumField), that allows you to treat almost any [PEP435](https://peps.python.org/pep-0435) enumeration as a database column. [EnumField](https://django-enum.rtfd.io/en/stable/reference/fields.html#django_enum.fields.EnumField) resolves the correct native [Django](https://www.djangoproject.com) field type for the given enumeration based on its value type and range. For example, [IntegerChoices](https://docs.djangoproject.com/en/stable/ref/models/fields/#field-choices-enum-types) that contain values between 0 and 32767 become [PositiveSmallIntegerField](https://docs.djangoproject.com/en/stable/ref/models/fields/#positivesmallintegerfield).

```python
from django.db import models
from django_enum import EnumField

class MyModel(models.Model):

    class TextEnum(models.TextChoices):

        VALUE0 = 'V0', 'Value 0'
        VALUE1 = 'V1', 'Value 1'
        VALUE2 = 'V2', 'Value 2'

    class IntEnum(models.IntegerChoices):

        ONE   = 1, 'One'
        TWO   = 2, 'Two',
        THREE = 3, 'Three'

    # this is equivalent to:
    #  CharField(max_length=2, choices=TextEnum.choices, null=True, blank=True)
    txt_enum = EnumField(TextEnum, null=True, blank=True)

    # this is equivalent to
    #  PositiveSmallIntegerField(choices=IntEnum.choices, default=IntEnum.ONE.value)
    int_enum = EnumField(IntEnum, default=IntEnum.ONE)
```

[EnumField](https://django-enum.rtfd.io/en/stable/reference/fields.html#django_enum.fields.EnumField) **is more than just an alias. The fields are now assignable and accessible as their enumeration type rather than by-value:**

```python
instance = MyModel.objects.create(
    txt_enum=MyModel.TextEnum.VALUE1,
    int_enum=3  # by-value assignment also works
)

assert instance.txt_enum == MyModel.TextEnum('V1')
assert instance.txt_enum.label == 'Value 1'

assert instance.int_enum == MyModel.IntEnum['THREE']
assert instance.int_enum.value == 3
```

## Flag Support (BitFields)

[Flag](https://docs.python.org/3/library/enum.html#enum.Flag) types are also seamlessly supported! This allows a database column to behave like a bit field and is an alternative to having multiple boolean columns. There are positive performance implications for using a bit field instead of booleans proportional on the size of the bit field and the types of queries you will run against it. For bit fields more than a few bits long the size reduction both speeds up queries and reduces the required storage space. See the documentation for [discussion and benchmarks](https://django-enum.readthedocs.io/en/latest/performance.html#flags).

```python
class Permissions(IntFlag):

    READ    = 1 << 0
    WRITE   = 1 << 1
    EXECUTE = 1 << 2


class FlagExample(models.Model):

    permissions = EnumField(Permissions)


FlagExample.objects.create(permissions=Permissions.READ | Permissions.WRITE)

# get all models with RW:
FlagExample.objects.filter(permissions__has_all=Permissions.READ | Permissions.WRITE)
```

## Complex Enumerations

[django-enum](https://pypi.org/project/django-enum) supports enum types that do not derive from Django's [IntegerChoices](https://docs.djangoproject.com/en/stable/ref/models/fields/#field-choices-enum-types) and [TextChoices](https://docs.djangoproject.com/en/stable/ref/models/fields/#field-choices-enum-types). This allows us to use other libs like [enum-properties](https://pypi.org/project/enum-properties) which makes possible very rich enumeration fields:

``?> pip install enum-properties``

```python
from enum_properties import StrEnumProperties
from django.db import models

class TextChoicesExample(models.Model):

    class Color(StrEnumProperties):

        # attribute type hints become properties on each value,
        # and the enumeration may be instantiated from any symmetric
        # property's value

        label: Annotated[str, Symmetric()]
        rgb: Annotated[t.Tuple[int, int, int], Symmetric()]
        hex: Annotated[str, Symmetric(case_fold=True)]

        # properties specified in type hint order after the value
        # name value label       rgb       hex
        RED   = "R", "Red",   (1, 0, 0), "ff0000"
        GREEN = "G", "Green", (0, 1, 0), "00ff00"
        BLUE  = "B", "Blue",  (0, 0, 1), "0000ff"

    color = EnumField(Color)

instance = TextChoicesExample.objects.create(
    color=TextChoicesExample.Color('FF0000')
)
assert instance.color == TextChoicesExample.Color('Red')
assert instance.color == TextChoicesExample.Color('R')
assert instance.color == TextChoicesExample.Color((1, 0, 0))

# direct comparison to any symmetric value also works
assert instance.color == 'Red'
assert instance.color == 'R'
assert instance.color == (1, 0, 0)

# save by any symmetric value
instance.color = 'FF0000'

# access any enum property right from the model field
assert instance.color.hex == 'ff0000'

# this also works!
assert instance.color == 'ff0000'

# and so does this!
assert instance.color == 'FF0000'

instance.save()

# filtering works by any symmetric value or enum type instance
assert TextChoicesExample.objects.filter(
    color=TextChoicesExample.Color.RED
).first() == instance

assert TextChoicesExample.objects.filter(color=(1, 0, 0)).first() == instance

assert TextChoicesExample.objects.filter(color='FF0000').first() == instance
```

While they should be unnecessary if you need to integrate with code that expects an interface fully compatible with Django's [TextChoices](https://docs.djangoproject.com/en/stable/ref/models/fields/#field-choices-enum-types) and [IntegerChoices](https://docs.djangoproject.com/en/stable/ref/models/fields/#field-choices-enum-types) [django-enum](https://pypi.org/project/django-enum) provides [TextChoices](https://django-enum.rtfd.io/en/stable/reference/choices.html#django_enum.choices.TextChoices), [IntegerChoices](https://django-enum.rtfd.io/en/stable/reference/choices.html#django_enum.choices.IntegerChoices), [FlagChoices](https://django-enum.rtfd.io/en/stable/reference/choices.html#django_enum.choices.FlagChoices) and [FloatChoices](https://django-enum.rtfd.io/en/stable/reference/choices.html#django_enum.choices.FloatChoices) types that derive from enum-properties and Django's ``Choices``. So the above enumeration could also be written:

```python
from django_enum.choices import TextChoices

class Color(TextChoices):

    # label is added as a symmetric property by the base class

    rgb: Annotated[t.Tuple[int, int, int], Symmetric()]
    hex: Annotated[str, Symmetric(case_fold=True)]

    # name value label       rgb       hex
    RED   = "R", "Red",   (1, 0, 0), "ff0000"
    GREEN = "G", "Green", (0, 1, 0), "00ff00"
    BLUE  = "B", "Blue",  (0, 0, 1), "0000ff"

```

## Installation

1. Clone django-enum from [GitHub](https://github.com/django-commons/django-enum) or install a release off [pypi](https://pypi.org/project/django-enum):

```bash
   pip install django-enum
```

[django-enum](https://pypi.org/project/django-enum) has several optional dependencies that are not installed by default. [EnumField](https://django-enum.rtfd.io/en/stable/reference/fields.html#django_enum.fields.EnumField) works seamlessly with all Django apps that work with model fields with choices without any additional work. Optional integrations are provided with several popular libraries to extend this basic functionality, these include:


* [enum-properties](https://pypi.org/project/enum-properties)
    ```bash
    > pip install "django-enum[properties]"
    ```
* [django-filter](https://pypi.org/project/django-filter)
* [djangorestframework](https://www.django-rest-framework.org)


## Database Support

[![Postgres](https://img.shields.io/badge/Postgres-9.6%2B-blue)](https://www.postgresql.org/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7%2B-blue)](https://www.mysql.com/)
[![MariaDB](https://img.shields.io/badge/MariaDB-10.2%2B-blue)](https://mariadb.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.8%2B-blue)](https://www.sqlite.org/)
[![Oracle](https://img.shields.io/badge/Oracle-18%2B-blue)](https://www.oracle.com/database/)

Like with [Django](https://www.djangoproject.com), [PostgreSQL](https://www.postgresql.org) is the preferred database for support. The full test suite is run against all combinations of currently supported versions of [Django](https://www.djangoproject.com), [Python](https://www.python.org), and [PostgreSQL](https://www.postgresql.org) as well as [psycopg3](https://pypi.org/project/psycopg) and [psycopg2](https://pypi.org/project/psycopg2). The other RDBMS supported by [Django](https://www.djangoproject.com) are also tested including [SQLite](https://www.sqlite.org), [MySQL](https://www.mysql.com), [MariaDB](https://mariadb.org) and [Oracle](https://www.oracle.com/database). For these RDBMS (with the exception of [Oracle](https://www.oracle.com/database), tests are run against the minimum and maximum supported version combinations to maximize coverage breadth.

**See the [latest test runs](https://github.com/django-commons/django-enum/actions/workflows/test.yml) for our current test matrix**

For [Oracle](https://www.oracle.com/database), only the latest version of the free database is tested against the minimum and maximum supported versions of Python, Django and the [cx-Oracle](https://pypi.org/project/cx-Oracle) driver.

## Further Reading

Consider using [django-render-static](https://pypi.org/project/django-render-static) to make your enumerations [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) across the full stack!

Please report bugs and discuss features on the [issues page](https://github.com/django-commons/django-enum/issues).

[Contributions](https://github.com/django-commons/django-enum/blob/main/CONTRIBUTING.md) are encouraged!

[Full documentation at read the docs.](https://django-enum.readthedocs.io)