.. include:: ../refs.rst

.. _flag_enums:

=====================
Use Flags (BitFields)
=====================

Python supports `bit fields <https://en.wikipedia.org/wiki/Bit_field>`_ through the
:class:`enum.Flag` extension to :class:`enum.Enum`.

These enumerations are fully supported and will render as multi select form fields by default. For
example:

.. _group_permissions_ex:

.. literalinclude:: ../../../tests/examples/models/flag_howto.py
    :lines: 2-

.. literalinclude:: ../../../tests/examples/flag_howto.py
    :lines: 14-22

**Two new field lookups are provided for flag enumerations:** :ref:`has_any` **and** :ref:`has_all`.

.. _has_any:

has_any
-------

The :ref:`has_any` lookup will return any object that has at least one of the flags in the
referenced enumeration. For example:

.. literalinclude:: ../../../tests/examples/flag_howto.py
    :lines: 23-30

.. _has_all:

has_all
-------

The :ref:`has_all` lookup will return any object that has at least all of the flags in the
referenced enumeration. For example:

.. literalinclude:: ../../../tests/examples/flag_howto.py
    :lines: 32-

**There are performance considerations when using a bit mask like a Flag enumeration instead of
multiple boolean columns.** See :ref:`flag performance <flag_performance>` for discussion and
benchmarks.

.. _full_width_flags:

Flags that use the sign bit
---------------------------

Most databases have no unsigned integer types, but a bit field has no use for a sign. Flag fields
are therefore stored in a *signed* column of 16, 32 or 64 bits and the value is two's complemented
on the way in and out, so that every bit of the column is available:

.. code-block:: python

    class Permissions(IntFlag):
        READ = 1 << 0
        WRITE = 1 << 1
        # ...
        ADMIN = 1 << 31  # the sign bit of a 32 bit column

    class Widget(models.Model):
        permissions = EnumField(Permissions)  # -> IntegerFlagField

    widget = Widget.objects.create(permissions=Permissions.ADMIN | Permissions.READ)
    Widget.objects.filter(permissions__has_all=Permissions.ADMIN | Permissions.READ)

In python the value is always the non-negative ``Permissions.ADMIN | Permissions.READ``, the
database column holds ``-2147483647``. Lookups, ``update()`` values and check constraints are
converted automatically. An enumeration with up to 16 flags gets a 16 bit column, up to 32 flags a
32 bit column and up to 64 flags a 64 bit column.

.. note::

    Django resolves the type of a bare value inside an :class:`~django.db.models.F` expression
    from the python value, not from the field, so a flag with the sign bit set is not converted
    there. Wrap it in a :class:`~django.db.models.Value` with the field as the ``output_field``:

    .. code-block:: python

        from django.db.models import F, Value

        Widget.objects.update(
            permissions=F("permissions").bitor(
                Value(Permissions.ADMIN, output_field=Widget._meta.get_field("permissions"))
            )
        )

    MySQL and MariaDB evaluate bitwise operators as unsigned 64 bit integers, so bitwise
    :class:`~django.db.models.F` updates involving the sign bit do not work on those databases at
    all. Assign the value instead.

.. _large_flags:

Flags with more than 64 bits
----------------------------

Flag enumerations of arbitrary size are supported, however if the enum has more than 64 flags it
will be stored as a :class:`~django.db.models.BinaryField`. It is therefore strongly recommended to
keep your :class:`enum.IntFlag` enumerations at 64 bits or less.

.. warning::

    Support for extra large flag fields is experimental. :ref:`has_any` and :ref:`has_all` do not
    work. Most RDBMS systems do not support bitwise operations on binary fields. Future work may
    involve exploring support for this as a Postgres extension.
