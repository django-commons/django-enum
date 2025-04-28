.. include:: ../refs.rst

.. _admin:

================
Use Django Admin
================

:class:`~django_enum.fields.EnumField` will mostly just work in the Django
:mod:`~django.contrib.admin`. There is
`one issue <https://github.com/django-commons/django-enum/issues/123>`_ where :ref:`enums that are
not hash equivalent <hash_equivalency>` will not render value labels correctly in the
:class:`~django.contrib.admin.ModelAdmin` :attr:`~django.contrib.admin.ModelAdmin.list_display`.
