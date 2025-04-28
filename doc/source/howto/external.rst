.. include:: ../refs.rst

.. _external:

==================
Use External Enums
==================

:class:`enum.Enum` classes defined externally to your code base or enum classes that otherwise do
not inherit from Django's :ref:`field-choices-enum-types`, are supported. When no choices are
present on an :class:`enum.Enum` type, :class:`~django_enum.fields.EnumField` will attempt to use
the ``label`` member on each enumeration value if it is present, otherwise the labels will be based
off the enumeration name. Choices can also be overridden at the
:class:`~django_enum.fields.EnumField` declaration.

:class:`~django_enum.fields.EnumField` should work with any subclass of :class:`enum.Enum`.

.. literalinclude:: ../../../tests/examples/models/extern.py

The list of choice tuples for each field are:

.. literalinclude:: ../../../tests/examples/extern_howto.py
    :lines: 3-

.. warning::

    One nice feature of Django's :ref:`field-choices-enum-types` are that they disable
    :class:`enum.auto` on :class:`enum.Enum` fields. :class:`enum.auto` can be dangerous because the
    values assigned depend on the order of declaration. This means that if the order changes
    existing database values will no longer align with the enumeration values. When control over the
    values is not certain it is a good idea to add integration tests that look for value changes.

.. _hash_equivalency:

Hash Equivalency
----------------

.. tip::

    It is a good idea to make sure your enumeration instances are hash equivalent to their
    primitive values. You can do this simply by inheriting from their primitive value
    (e.g. ``class MyEnum(str, Enum):``) or by using :class:`~enum.StrEnum` and
    :class:`~enum.IntEnum` types. Any enumeration defined using :doc:`enum-properties:index`
    will be hash equivalent to its values by default.

:class:`~django_enum.fields.EnumField` automatically sets the choices tuple on the field. Django_
has logic in a number of places that handles fields with choices in a special way
(e.g. :ref:`in the admin <admin>`). For example, the choices may be converted to a dictionary
mapping values to labels. The values will be the primitive values of the enumeration not
enumeration instances and the current value of the field which may be an enumeration instance will
be searched for in the dictionary. This will fail if the enumeration instance is not hash
equivalent to its value.

To control the hashing behavior of an object, you must override its :meth:`~object.__hash__` and
:meth:`~object.__eq__` methods.

For example:

.. literalinclude:: ../../../tests/examples/models/hash_equivalency.py

.. literalinclude:: ../../../tests/examples/hash_equivalency_howto.py
    :lines: 3-
