.. include:: refs.rst

==========
Change Log
==========

v2.2.4 (2025-09-21)
===================

* Implemented `Support Python 3.14 <https://github.com/django-commons/django-enum/issues/135>`_
* Fixed `Avoid depending on typing_extensions. <https://github.com/django-commons/django-enum/pull/134>`_

v2.2.3 (2025-04-28)
===================

* Add docs on hash equivalency, fixing `Enum value doesn't show in Django Admin's list_display <https://github.com/django-commons/django-enum/issues/123>`_

v2.2.2 (2025-04-18)
===================

* Minor doc fixes.

v2.2.1 (2025-04-18)
===================

* First release under `django-commons <https://github.com/django-commons>`_ ownership!
* Fix all links to reflect new home @ `django-commons <https://github.com/django-commons>`_

v2.2.0 (2025-03-28)
===================

* Implemented `Need a DRF integration for FlagFields <https://github.com/django-commons/django-enum/issues/113>`_
* Fixed `FilterSet override of filter_for_lookup disregards meta options. <https://github.com/django-commons/django-enum/issues/111>`_
* Implemented `Add EnumFlagFilter to support has_any and has_all flag queries. <https://github.com/django-commons/django-enum/issues/110>`_
* Fixed `Enum types that resolve to primitives of str or int but that do not inherit from those types can result in validation errors. <https://github.com/django-commons/django-enum/issues/109>`_
* Implemented `Support checkboxes for FlagEnumField <https://github.com/django-commons/django-enum/issues/107>`_
* Implemented `Support radio buttons for EnumChoiceField <https://github.com/django-commons/django-enum/issues/106>`_
* Implemented `If default is not provided for flag fields it should be Flag(0). <https://github.com/django-commons/django-enum/issues/105>`_
* Fixed `EnumFlagFields set empty values to Flag(0) when model field has null=True, default=None <https://github.com/django-commons/django-enum/issues/104>`_
* Fixed `Large enum fields that inherit from binaryfield have editable=False by default <https://github.com/django-commons/django-enum/issues/103>`_
* Fixed `EnumFlagField breaks for Flag types that are not constructible from lists of values <https://github.com/django-commons/django-enum/issues/102>`_
* Implemented `Test all example code in the docs <https://github.com/django-commons/django-enum/issues/99>`_
* Implemented `Use intersphinx for doc references <https://github.com/django-commons/django-enum/issues/98>`_
* Implemented `Support Django 5.2 <https://github.com/django-commons/django-enum/issues/96>`_
* Implemented `Upgrade to enum-properties >=2.2 <https://github.com/django-commons/django-enum/issues/95>`_
* Implemented `Move form imports to locally scoped imports where needed in fields.py <https://github.com/django-commons/django-enum/issues/79>`_
* Implemented `Reorganize documentation using diataxis <https://github.com/django-commons/django-enum/issues/72>`_
* Implemented `Provide a MultipleEnumChoiceFilter <https://github.com/django-commons/django-enum/issues/25>`_
* Implemented `Provide an EnumMultipleChoiceField <https://github.com/django-commons/django-enum/issues/24>`_

v2.1.0 (2025-02-24)
===================

* Implemented `Switch poetry -> uv <https://github.com/django-commons/django-enum/issues/87>`_
* Implemented `Add macos runner to CI <https://github.com/django-commons/django-enum/issues/86>`_
* Implemented `Add windows runner to CI <https://github.com/django-commons/django-enum/issues/85>`_
* Implemented `Drop support for python 3.8 <https://github.com/django-commons/django-enum/issues/84>`_
* Implemented `Move to justfile dev interface. <https://github.com/django-commons/django-enum/issues/83>`_
* Implemented `Modernize pyproject.toml <https://github.com/django-commons/django-enum/issues/82>`_

v2.0.2 (2024-09-25)
===================

* Fixed `Constraints fail when using a name argument <https://github.com/django-commons/django-enum/issues/77>`_

v2.0.1 (2024-09-16)
===================

* Fixed `Unexpected ValueError instead of ValidationError <https://github.com/django-commons/django-enum/issues/74>`_

v2.0.0 (2024-09-09)
===================

* Completed `Reorganize tests <https://github.com/django-commons/django-enum/issues/70>`_
* Completed `Switch linting and formatting to ruff <https://github.com/django-commons/django-enum/issues/62>`_
* Implemented `Install django-stubs when running static type checks. <https://github.com/django-commons/django-enum/issues/60>`_
* Fixed `When a character enum field allows null and blank=True, form fields and drf fields allow '' to pass through causing errors. <https://github.com/django-commons/django-enum/issues/53>`_
* Implemented `Supply a mixin for DRF ModelSerializers that instantiates the provided DRF EnumField type for model EnumFields. <https://github.com/django-commons/django-enum/issues/47>`_
* Implemented `EnumField's should inherit from common base titled EnumField <https://github.com/django-commons/django-enum/issues/46>`_
* Implemented `Add database constraints on enum fields by default. <https://github.com/django-commons/django-enum/issues/45>`_
* Fixed `to_python() raises ValueError instead of spec'ed ValidationError <https://github.com/django-commons/django-enum/issues/44>`_
* Implemented `Add support for date, datetime, timedelta, time and Decimal enumeration types. <https://github.com/django-commons/django-enum/issues/43>`_
* Fixed `None should be an allowable enumeration value in enums of any primitive type. <https://github.com/django-commons/django-enum/issues/42>`_
* Implemented `Characterize the performance trade offs of bitfields vs indexed and non-indexed boolean fields. <https://github.com/django-commons/django-enum/issues/41>`_
* Fixed `When coerce is false, to_python does not convert to the Enum's primitive type <https://github.com/django-commons/django-enum/issues/39>`_
* Implemented `Provide parameter to override integer range on EnumField. <https://github.com/django-commons/django-enum/issues/38>`_
* Implemented `Add all official supported Django RDBMS backends to CI <https://github.com/django-commons/django-enum/issues/33>`_
* Implemented `Support for integer sizes greater than 64 bit <https://github.com/django-commons/django-enum/issues/32>`_
* Implemented `Provide an optional enum path converter. <https://github.com/django-commons/django-enum/issues/22>`_
* Implemented `Support flag enumerations <https://github.com/django-commons/django-enum/issues/7>`_

.. _migration_1.x_to_2.x:

Migration from 1.x -> 2.x
-------------------------

* Imports of :doc:`enum-properties:index` extended ``TextChoices`` and ``IntegerChoices`` have been
  changed:

    .. code-block:: python

        # 1.x way
        from django_enum import TextChoices, IntegerChoices

        # 2.x way
        from django_enum.choices import TextChoices, IntegerChoices

* Imports of ``EnumChoiceField`` for django forms has been changed:

    .. code-block:: python

        # 1.x way
        from django_enum import EnumChoiceField

        # 2.x way
        from django_enum.forms import EnumChoiceField

* Imports of ``EnumFilter`` and ``FilterSet`` has been changed:

    .. code-block:: python

        # 1.x way
        from django_enum import EnumFilter, FilterSet

        # 2.x way
        from django_enum.filters import EnumFilter, FilterSet


* Strict :class:`~django_enum.fields.EnumField` values are now constrained at the database level
  using `CheckConstraints <https://docs.djangoproject.com/en/stable/ref/models/constraints/>`_
  by default. To disable this behavior, set the ``constrained`` parameter to ``False``.

v1.3.3 (2024-08-26)
===================

* Implemented `Support python 3.13 <https://github.com/django-commons/django-enum/issues/67>`_
* Implemented `Drop support for Python 3.7 <https://github.com/django-commons/django-enum/issues/68>`_

v1.3.2 (2024-07-15)
===================

* Fixed `Support Django 5.1 <https://github.com/django-commons/django-enum/issues/63>`_


v1.3.1 (2024-03-02)
===================

* Fixed `db_default produces expressions instead of primitives when given enum value instances. <https://github.com/django-commons/django-enum/issues/59>`_

v1.3.0 (2023-12-13)
===================

* Implemented `Support db_default <https://github.com/django-commons/django-enum/issues/56>`_
* Fixed `When coerce=False, enum form fields and model fields should still coerce to the enum's primitive type. <https://github.com/django-commons/django-enum/issues/55>`_
* Implemented `Support Django 5.0 <https://github.com/django-commons/django-enum/issues/54>`_

v1.2.2 (2023-10-02)
===================

* Added `Support python 3.12. <https://github.com/django-commons/django-enum/issues/52>`_
* Fixed `EnumFields don't display correctly in the Admin when set to read_only. <https://github.com/django-commons/django-enum/issues/35>`_

v1.2.1 (2023-04-08)
===================

* Fixed `Document that with version 1.4 of enum-properties label is no longer overridable for Choices <https://github.com/django-commons/django-enum/issues/37>`_

v1.2.0 (2023-04-02)
===================

* Implemented `Compat for enums not deriving from Django's choices. <https://github.com/django-commons/django-enum/issues/34>`_


v1.1.2 (2023-02-15)
===================

* Fixed `LICENSE packaged into source dir. <https://github.com/django-commons/django-enum/issues/23>`_

v1.1.1 (2023-01-15)
===================

* Fixed `Broken on Django4.1/Python 3.11. <https://github.com/django-commons/django-enum/issues/17>`_

v1.1.0 (2022-08-13)
===================

* Fixed `django-filter intergration for non-strict values does not work. <https://github.com/django-commons/django-enum/issues/6>`_
* Implemented `Set EnumChoiceField to the default form field type. <https://github.com/django-commons/django-enum/issues/5>`_
* Implemented `Coerce default values to Enum types. <https://github.com/django-commons/django-enum/issues/4>`_
* Implemented `Use custom descriptor to coerce fields to Enum type on assignment. <https://github.com/django-commons/django-enum/issues/3>`_

v1.0.1 (2022-08-11)
===================

* Fix dependency issue - allow python 3.6


v1.0.0 (2022-08-11)
===================

* Initial Re-Release (production/stable)


v0.1.0 (2010-09-18)
===================

* Legacy django-enum library maintained by `Jacob Smullyan <https://pypi.org/user/smulloni>`_.
  Source located `here <https://github.com/smulloni/django-enum-old>`_.
