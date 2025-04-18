.. include:: refs.rst

===========
Django Enum
===========

|MIT license| |Ruff| |PyPI version fury.io| |PyPI pyversions| |PyPi djversions| |PyPI status|
|Documentation Status| |Code Cov| |Test Status| |Django Packages|


|Postgres| |MySQL| |MariaDB| |SQLite| |Oracle|

.. |MIT license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://lbesson.mit-license.org/

.. |Ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://docs.astral.sh/ruff

.. |PyPI version fury.io| image:: https://badge.fury.io/py/django-enum.svg
   :target: https://pypi.python.org/pypi/django-enum/

.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/django-enum.svg
   :target: https://pypi.python.org/pypi/django-enum/

.. |PyPI djversions| image:: https://img.shields.io/pypi/djversions/django-enum.svg
   :target: https://pypi.org/project/django-enum/

.. |PyPI status| image:: https://img.shields.io/pypi/status/django-enum.svg
   :target: https://pypi.python.org/pypi/django-enum

.. |Documentation Status| image:: https://readthedocs.org/projects/django-enum/badge/?version=latest
   :target: http://django-enum.readthedocs.io/?badge=latest/

.. |Code Cov| image:: https://codecov.io/gh/django-commons/django-enum/branch/main/graph/badge.svg?token=0IZOKN2DYL
   :target: https://codecov.io/gh/django-commons/django-enum

.. |Test Status| image:: https://github.com/django-commons/django-enum/workflows/test/badge.svg
   :target: https://github.com/django-commons/django-enum/actions/workflows/test.yml

.. |Lint Status| image:: https://github.com/django-commons/django-enum/workflows/lint/badge.svg
   :target: https://github.com/django-commons/django-enum/actions/workflows/lint.yml

.. |Django Packages| image:: https://img.shields.io/badge/Published%20on-Django%20Packages-0c3c26
    :target: https://djangopackages.org/packages/p/django-enum/

.. |Postgres| image:: https://img.shields.io/badge/Postgres-9.6%2B-blue
   :target: https://www.postgresql.org/

.. |MySQL| image:: https://img.shields.io/badge/MySQL-5.7%2B-blue
    :target: https://www.mysql.com

.. |MariaDB| image:: https://img.shields.io/badge/MariaDB-10.2%2B-blue
    :target: https://mariadb.org/

.. |SQLite| image:: https://img.shields.io/badge/SQLite-3.8%2B-blue
    :target: https://www.sqlite.org/

.. |Oracle| image:: https://img.shields.io/badge/Oracle-18%2B-blue
    :target: https://www.oracle.com/database/

----

.. tip::

    See :ref:`migration_1.x_to_2.x` for how to update from 1.x to 2.x.

Full and natural support for PEP435_ :class:`enumerations <enum.Enum>` as Django_ model fields.

Many packages aim to ease usage of Python enumerations as model fields. Most were superseded when
Django provided :ref:`TextChoices <field-choices-enum-types>` and
:ref:`IntegerChoices <field-choices-enum-types>` types. The motivation for django-enum_ was to:

* Work with any :class:`~enum.Enum` including those that do not derive from
  Django's :ref:`TextChoices <field-choices-enum-types>` and
  :ref:`IntegerChoices <field-choices-enum-types>`.
* Coerce fields to instances of the :class:`~enum.Enum` type by default.
* Allow strict adherence to :class:`~enum.Enum` values to be disabled.
* Handle migrations appropriately. (See :ref:`migrations`)
* Integrate as fully as possible with Django's
  :ref:`existing level of enum support <field-choices-enum-types>`.
* Support :doc:`enum-properties:index` to enable richer enumeration types. (A less awkward
  alternative to :ref:`dataclass enumerations <enum-dataclass-support>` with more features)
* Represent enum fields with the smallest possible column type.
* Support `bit field <https://en.wikipedia.org/wiki/Bit_field>`_ queries using standard
  :class:`Python Flag enumerations <enum.Flag>`.
* Be as simple and light-weight an extension to core Django_ as possible.
* Enforce enumeration value consistency at the database level using
  :doc:`check constraints <django:ref/models/constraints>` by default.
* (TODO) Support native database enumeration column types when available.

django-enum_ provides a new model field type, :class:`~django_enum.fields.EnumField`, that allows
you to treat almost any PEP435_ enumeration as a database column.
:class:`~django_enum.fields.EnumField` resolves the correct native Django_ field type for the given
enumeration based on its value type and range. For example,
:ref:`IntegerChoices <field-choices-enum-types>` that contain values between 0 and 32767 become
:class:`~django.db.models.PositiveSmallIntegerField`.

.. literalinclude:: ../../tests/examples/models/basic.py
    :language: python
    :lines: 2-

:class:`~django_enum.fields.EnumField` **is more than just an alias. The fields are now assignable
and accessible as their enumeration type rather than by-value:**

.. literalinclude:: ../../tests/examples/basic_example.py
    :language: python
    :lines: 2-

Flag Support (BitFields)
========================

:class:`enum.Flag` types are also seamlessly supported! This allows a database column to behave
like a bit field and is an alternative to having multiple boolean columns. There are positive
performance implications for using a bit field instead of booleans proportional on the size of the
bit field and the types of queries you will run against it. For bit fields more than a few bits long
the size reduction both speeds up queries and reduces the required storage space. See the
documentation for :ref:`discussion and benchmarks <flag_performance>`.

.. literalinclude:: ../../tests/examples/models/flag.py
    :language: python
    :lines: 2-

.. literalinclude:: ../../tests/examples/flag_example.py
    :language: python
    :lines: 4-

.. note::

    The :ref:`has_all` and :ref:`has_any` field lookups are only available for Flag enumerations.

Enums with Properties
=====================

django-enum_ supports enum types that do not derive from Django's
:ref:`IntegerChoices <field-choices-enum-types>` and :ref:`TextChoices <field-choices-enum-types>`.
This allows us to use other libs like :doc:`enum-properties:index` which makes possible very
rich enumeration fields:

.. code-block:: bash

    > pip install enum-properties


.. literalinclude:: ../../tests/examples/models/properties.py
    :language: python
    :lines: 2-

.. literalinclude:: ../../tests/examples/properties_example.py
    :language: python
    :lines: 4-

While they should be unnecessary, if you need to integrate with code that expects an interface fully
compatible with Django's :ref:`TextChoices <field-choices-enum-types>` and
:ref:`IntegerChoices <field-choices-enum-types>` django-enum_
provides :class:`~django_enum.choices.TextChoices`, :class:`~django_enum.choices.IntegerChoices`,
:class:`~django_enum.choices.FlagChoices` and :class:`~django_enum.choices.FloatChoices` types that
derive from :doc:`enum-properties:index` and Django's ``Choices``. So the above enumeration could
also be written:

.. literalinclude:: ../../tests/examples/models/properties_choices.py
    :language: python
    :lines: 7-


Installation
============

1. Clone django-enum from GitHub_ or install a release off PyPI_:

.. code-block:: bash

   > pip install django-enum


django-enum_ has several optional dependencies that are not installed by default.
:class:`~django_enum.fields.EnumField` works seamlessly with all Django apps that work with model
fields with choices without any additional work. Optional integrations are provided with several
popular libraries to extend this basic functionality, these include:

* :doc:`enum-properties <enum-properties:index>`
    .. code-block:: bash

        > pip install "django-enum[properties]"

* django-filter_
* djangorestframework_.


Database Support
================

|Postgres| |MySQL| |MariaDB| |SQLite| |Oracle|

Like with Django, PostgreSQL_ is the preferred database for support. The full test suite is run
against all combinations of currently supported versions of Django_, Python_, and PostgreSQL_ as
well as psycopg3_ and psycopg2_. The other RDBMS supported by Django_ are also tested including
SQLite_, MySQL_, MariaDB_ and Oracle_. For these RDBMS (with the exception of Oracle_), tests are
run against the minimum and maximum supported version combinations to maximize coverage breadth.

**See the** `latest test runs <https://github.com/django-commons/django-enum/actions/workflows/test.yml>`_
**for our current test matrix**

.. note::

    For Oracle_, only the latest version of the free database is tested against the minimum and
    maximum supported versions of Python, Django and the cx-Oracle_ driver.

Further Reading
===============

Consider using :doc:`django-render-static <django-render-static:index>` to make your enumerations
DRY_ across the full stack!

Please report bugs and discuss features on the
`issues page <https://github.com/django-commons/django-enum/issues>`_.

`Contributions <https://github.com/django-commons/django-enum/blob/main/CONTRIBUTING.md>`_ are encouraged!


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorials/index.rst
   howto/index.rst
   performance
   eccentric
   reference/index
   changelog
