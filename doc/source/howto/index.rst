.. include:: ../refs.rst

======
How To
======

:class:`~django_enum.fields.EnumField` infers the primitive enumeration type and maps to the most
appropriate Django_ field type. For example :class:`enum.StrEnum` types would become
:class:`~django.db.models.CharField` and :class:`enum.IntEnum` types would become
:class:`~django.db.models.PositiveSmallIntegerField` or
:class:`~django.db.models.PositiveIntegerField` depending on the maximum enumeration value.

This means that :class:`~django_enum.fields.EnumField` columns will behave as expected and integrate
broadly with third party libraries. When issues arise it tends to be because the primitive type was
marshalled into an :class:`enum.Enum` instance. :ref:`integrations` with some popular third party
libraries are provided.

For example:

.. literalinclude:: ../../../tests/examples/models/equivalency.py


``txt_enum`` and ``txt_choices`` fields are equivalent in all ways with the
following exceptions:

.. literalinclude:: ../../../tests/examples/equivalency_howto.py
    :lines: 5-


:class:`~django.forms.ModelForm` classes, DRF_ serializers and filters will behave the same way
with ``txt_enum`` and ``txt_choices``. A few types are provided for deeper integration with forms
and django-filter_ but their usage is optional. See :ref:`forms` and :ref:`filtering`.

Very rich enumeration fields that encapsulate much more functionality in a simple declarative syntax
are possible with :class:`~django_enum.fields.EnumField`. See :ref:`enum_props`.

.. toctree::
   :maxdepth: 2
   :caption: How Tos:

   external
   options
   flags
   forms
   integrations
   migrations
   urls
   admin
