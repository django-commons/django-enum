import sys
import pytest
from django.test import TestCase
from tests.djenum.models import EnumFlagTester, EnumFlagTesterRelated
from django_enum.fields import EnumField, FlagField, ExtraBigIntegerFlagField
from django.db.models import F, Q, Func, OuterRef, Subquery, Count
from django.db.utils import DatabaseError
from tests.utils import IGNORE_ORA_00932
from django.db import connection
from django.core.exceptions import FieldError


def combine_flags(*flags):
    if flags:
        flag = flags[0]
        for flg in flags[1:]:
            flag = flag | flg
        return flag
    return 0


def invert_flags(en):
    # invert a flag enumeration. in python 3.11+ ~ operator is supported
    if sys.version_info >= (3, 11, 4) and en.value > 0:
        return ~en
    return en.__class__(
        combine_flags(
            *[
                flag
                for flag in list(en.__class__.__members__.values())
                if flag not in en
            ]
        )
    )


class FlagTests(TestCase):
    MODEL_CLASS = EnumFlagTester
    RELATED_CLASS = EnumFlagTesterRelated

    def test_flag_filters(self):
        fields = [
            field
            for field in self.MODEL_CLASS._meta.fields
            if isinstance(field, EnumField)
        ]

        # keep track of empty counts for filter assertions
        empties = {field.name: 0 for field in fields}

        def update_empties(obj):
            for field in fields:
                value = getattr(obj, field.name)
                if value is not None and int(value) == 0:
                    empties[field.name] += 1

        obj0 = self.MODEL_CLASS.objects.create()
        update_empties(obj0)

        null_qry = self.MODEL_CLASS.objects.filter(small_pos__isnull=True)
        self.assertEqual(null_qry.count(), 1)
        self.assertEqual(null_qry.first(), obj0)
        self.assertIsNone(null_qry.first().small_pos)

        for field in [
            field.name
            for field in fields
            if isinstance(field, FlagField)
            and not isinstance(field, ExtraBigIntegerFlagField)
        ]:
            EnumClass = self.MODEL_CLASS._meta.get_field(field).enum

            empty = self.MODEL_CLASS.objects.create(**{field: EnumClass(0)})
            update_empties(empty)

            # Create the model
            obj = self.MODEL_CLASS.objects.create(**{field: EnumClass.ONE})
            update_empties(obj)

            # does this work in SQLite?
            if "extra" not in field:
                self.MODEL_CLASS.objects.filter(pk=obj.pk).update(
                    **{field: F(field).bitor(EnumClass.TWO)}
                )
            else:
                for obj in self.MODEL_CLASS.objects.filter(pk=obj.pk):
                    setattr(obj, field, getattr(obj, field) | EnumClass.TWO)
                    obj.save()

            # Set flags manually
            self.MODEL_CLASS.objects.filter(pk=obj.pk).update(
                **{field: (EnumClass.ONE | EnumClass.THREE | EnumClass.FOUR)}
            )

            # Remove THREE (does not work in SQLite)
            if "extra" not in field:
                self.MODEL_CLASS.objects.filter(pk=obj.pk).update(
                    **{field: F(field).bitand(invert_flags(EnumClass.THREE))}
                )
            else:
                for obj in self.MODEL_CLASS.objects.filter(pk=obj.pk):
                    setattr(
                        obj, field, getattr(obj, field) & invert_flags(EnumClass.THREE)
                    )
                    obj.save()

            # Find by awesome_flag
            fltr = self.MODEL_CLASS.objects.filter(
                **{field: (EnumClass.ONE | EnumClass.FOUR)}
            )
            self.assertEqual(fltr.count(), 1)
            self.assertEqual(fltr.first().pk, obj.pk)
            self.assertEqual(
                getattr(fltr.first(), field), EnumClass.ONE | EnumClass.FOUR
            )

            if sys.version_info >= (3, 11):
                not_other = invert_flags(EnumClass.ONE | EnumClass.FOUR)
            else:
                not_other = EnumClass.TWO | EnumClass.THREE | EnumClass.FIVE

            fltr2 = self.MODEL_CLASS.objects.filter(**{field: not_other})
            self.assertEqual(fltr2.count(), 0)

            obj2 = self.MODEL_CLASS.objects.create(**{field: not_other})
            update_empties(obj2)
            self.assertEqual(fltr2.count(), 1)
            self.assertEqual(fltr2.first().pk, obj2.pk)
            self.assertEqual(getattr(fltr2.first(), field), not_other)

            obj3 = self.MODEL_CLASS.objects.create(
                **{
                    field: EnumClass.ONE | EnumClass.TWO,
                }
            )
            update_empties(obj3)

            for cont in [
                self.MODEL_CLASS.objects.filter(**{f"{field}__has_any": EnumClass.ONE}),
                self.MODEL_CLASS.objects.filter(**{f"{field}__has_all": EnumClass.ONE}),
            ]:
                self.assertEqual(cont.count(), 2)
                self.assertIn(obj3, cont)
                self.assertIn(obj, cont)
                self.assertNotIn(obj2, cont)

            cont2 = self.MODEL_CLASS.objects.filter(
                **{f"{field}__has_any": (EnumClass.ONE | EnumClass.TWO)}
            )
            self.assertEqual(cont2.count(), 3)
            self.assertIn(obj3, cont2)
            self.assertIn(obj2, cont2)
            self.assertIn(obj, cont2)

            cont3 = self.MODEL_CLASS.objects.filter(
                **{f"{field}__has_all": (EnumClass.ONE | EnumClass.TWO)}
            )
            self.assertEqual(cont3.count(), 1)
            self.assertIn(obj3, cont3)

            cont4 = self.MODEL_CLASS.objects.filter(
                **{f"{field}__has_all": (EnumClass.THREE | EnumClass.FIVE)}
            )
            self.assertEqual(cont4.count(), 1)
            self.assertIn(obj2, cont4)

            cont5 = self.MODEL_CLASS.objects.filter(
                **{f"{field}__has_all": (EnumClass.ONE | EnumClass.FIVE)}
            )
            self.assertEqual(cont5.count(), 0)

            cont6 = self.MODEL_CLASS.objects.filter(
                **{f"{field}__has_any": (EnumClass.FOUR | EnumClass.FIVE)}
            )
            self.assertEqual(cont6.count(), 2)
            self.assertIn(obj, cont6)
            self.assertIn(obj2, cont6)

            cont7 = self.MODEL_CLASS.objects.filter(
                **{f"{field}__has_any": EnumClass(0)}
            )
            self.assertEqual(cont7.count(), empties[field])
            self.assertIn(empty, cont7)

            cont8 = self.MODEL_CLASS.objects.filter(
                **{f"{field}__has_all": EnumClass(0)}
            )
            self.assertEqual(cont8.count(), empties[field])
            self.assertIn(empty, cont8)

            cont9 = self.MODEL_CLASS.objects.filter(**{field: EnumClass(0)})
            self.assertEqual(cont9.count(), empties[field])
            self.assertIn(empty, cont9)

            cont10 = self.MODEL_CLASS.objects.filter(
                **{f"{field}__exact": EnumClass(0)}
            )
            self.assertEqual(cont10.count(), empties[field])
            self.assertIn(empty, cont10)

        EnumClass = self.MODEL_CLASS._meta.get_field("pos").enum
        compound_qry = self.MODEL_CLASS.objects.filter(
            Q(small_pos__isnull=True) | Q(pos__has_any=EnumClass.ONE)
        )

        self.assertEqual(compound_qry.count(), 9)
        for obj in compound_qry:
            self.assertTrue(obj.small_pos is None or obj.pos & EnumClass.ONE)

        compound_qry = self.MODEL_CLASS.objects.filter(
            Q(small_pos__isnull=True) & Q(pos__has_any=EnumClass.ONE)
        )
        self.assertEqual(compound_qry.count(), 2)
        for obj in compound_qry:
            self.assertTrue(obj.small_pos is None and obj.pos & EnumClass.ONE)

    def test_subquery(self):
        """test that has_any and has_all work with complex queries involving subqueries"""

        for field in [
            field
            for field in self.MODEL_CLASS._meta.fields
            if isinstance(field, FlagField)
            and not isinstance(field, ExtraBigIntegerFlagField)
        ]:
            EnumClass = field.enum
            self.MODEL_CLASS.objects.all().delete()

            objects = [
                self.MODEL_CLASS.objects.create(
                    **{field.name: EnumClass.TWO | EnumClass.FOUR | EnumClass.FIVE}
                ),
                self.MODEL_CLASS.objects.create(
                    **{field.name: EnumClass.ONE | EnumClass.THREE}
                ),
                self.MODEL_CLASS.objects.create(
                    **{field.name: EnumClass.TWO | EnumClass.FOUR}
                ),
                self.MODEL_CLASS.objects.create(**{field.name: EnumClass.FIVE}),
                self.MODEL_CLASS.objects.create(
                    **{
                        field.name: (
                            EnumClass.ONE
                            | EnumClass.TWO
                            | EnumClass.THREE
                            | EnumClass.FOUR
                            | EnumClass.FIVE
                        )
                    }
                ),
            ]

            exact_matches = (
                self.MODEL_CLASS.objects.filter(
                    **{f"{field.name}__exact": OuterRef(field.name)}
                )
                .order_by()
                .annotate(count=Func(F("id"), function="Count"))
                .values("count")
            )

            any_matches = (
                self.MODEL_CLASS.objects.filter(
                    **{f"{field.name}__has_any": OuterRef(field.name)}
                )
                .order_by()
                .annotate(count=Func(F("id"), function="Count"))
                .values("count")
            )

            all_matches = (
                self.MODEL_CLASS.objects.filter(
                    **{f"{field.name}__has_all": OuterRef(field.name)}
                )
                .order_by()
                .annotate(count=Func(F("id"), function="Count"))
                .values("count")
            )

            for obj in self.MODEL_CLASS.objects.annotate(
                exact_matches=Subquery(exact_matches)
            ):
                self.assertEqual(obj.exact_matches, 1)

            for expected, obj in zip(
                [2, 2, 3, 3, 1],
                self.MODEL_CLASS.objects.annotate(
                    all_matches=Subquery(all_matches)
                ).order_by("id"),
            ):
                self.assertEqual(obj.all_matches, expected)

            for expected, obj in zip(
                [4, 2, 3, 3, 5],
                self.MODEL_CLASS.objects.annotate(
                    any_matches=Subquery(any_matches)
                ).order_by("id"),
            ):
                self.assertEqual(obj.any_matches, expected)

    def test_joins(self):
        """test that has_any and has_all work with complex queries involving joins"""
        working = []
        not_working = []
        for field in [
            field
            for field in self.MODEL_CLASS._meta.fields
            if isinstance(field, FlagField)
            and not isinstance(field, ExtraBigIntegerFlagField)
        ]:
            EnumClass = field.enum
            self.MODEL_CLASS.objects.all().delete()

            objects = [
                self.MODEL_CLASS.objects.create(
                    **{field.name: EnumClass.TWO | EnumClass.FOUR | EnumClass.FIVE}
                ),
                self.MODEL_CLASS.objects.create(
                    **{field.name: EnumClass.ONE | EnumClass.THREE}
                ),
                self.MODEL_CLASS.objects.create(
                    **{field.name: EnumClass.TWO | EnumClass.FOUR}
                ),
                self.MODEL_CLASS.objects.create(**{field.name: EnumClass.FIVE}),
                self.MODEL_CLASS.objects.create(
                    **{
                        field.name: (
                            EnumClass.ONE
                            | EnumClass.TWO
                            | EnumClass.THREE
                            | EnumClass.FOUR
                            | EnumClass.FIVE
                        )
                    }
                ),
            ]
            related = []
            for obj in objects:
                related.append(
                    [
                        self.RELATED_CLASS.objects.create(
                            **{
                                field.name: EnumClass.TWO
                                | EnumClass.FOUR
                                | EnumClass.FIVE
                            }
                        ),
                        self.RELATED_CLASS.objects.create(
                            **{field.name: EnumClass.ONE | EnumClass.THREE}
                        ),
                        self.RELATED_CLASS.objects.create(
                            **{field.name: EnumClass.TWO | EnumClass.FOUR}
                        ),
                        self.RELATED_CLASS.objects.create(
                            **{field.name: EnumClass.FIVE}
                        ),
                        self.RELATED_CLASS.objects.create(
                            **{
                                field.name: (
                                    EnumClass.ONE
                                    | EnumClass.TWO
                                    | EnumClass.THREE
                                    | EnumClass.FOUR
                                    | EnumClass.FIVE
                                )
                            }
                        ),
                    ]
                )
                for rel in related[-1]:
                    rel.related_flags.add(obj)
            try:
                for obj in self.MODEL_CLASS.objects.annotate(
                    exact_matches=Count(
                        "related_flags__id",
                        filter=Q(
                            **{f"related_flags__{field.name}__exact": F(field.name)}
                        ),
                    )
                ):
                    self.assertEqual(obj.exact_matches, 1)
            except DatabaseError as err:
                print(str(err))
                if (
                    IGNORE_ORA_00932
                    and connection.vendor == "oracle"
                    and ("ORA-00932" in str(err) or "ORA-22848" in str(err))
                ):
                    # this is an oracle bug - intermittent failure on
                    # perfectly fine date format in SQL
                    # TODO - remove when fixed
                    # pytest.skip("Oracle bug ORA-00932 encountered - skipping")
                    not_working.append(field.name)
                    # continue
                    pytest.skip(f"Oracle bug {err} encountered - skipping")
                raise

            working.append(field.name)

            for idx, (expected, obj) in enumerate(
                zip(
                    [2, 2, 3, 3, 1],
                    self.MODEL_CLASS.objects.annotate(
                        all_matches=Count(
                            "related_flags__id",
                            filter=Q(
                                **{
                                    f"related_flags__{field.name}__has_all": F(
                                        field.name
                                    )
                                }
                            ),
                        )
                    ).order_by("id"),
                )
            ):
                self.assertEqual(obj.all_matches, expected)

            for idx, (expected, obj) in enumerate(
                zip(
                    [4, 2, 3, 3, 5],
                    self.MODEL_CLASS.objects.annotate(
                        any_matches=Count(
                            "related_flags__id",
                            filter=Q(
                                **{
                                    f"related_flags__{field.name}__has_any": F(
                                        field.name
                                    )
                                }
                            ),
                        )
                    ).order_by("id"),
                )
            ):
                self.assertEqual(obj.any_matches, expected)

        if not_working:
            print(f"Fields not working: {not_working}")
            print(f"Fields working: {working}")

    def test_unsupported_flags(self):
        obj = self.MODEL_CLASS.objects.create()
        for field in ["small_neg", "neg", "big_neg", "extra_big_neg", "extra_big_pos"]:
            EnumClass = self.MODEL_CLASS._meta.get_field(field).enum
            with self.assertRaises(FieldError):
                self.MODEL_CLASS.objects.filter(**{"field__has_any": EnumClass.ONE})

            with self.assertRaises(FieldError):
                self.MODEL_CLASS.objects.filter(**{"field__has_all": EnumClass.ONE})

    def test_extra_big_flags(self):
        obj = self.MODEL_CLASS.objects.create()
        self.assertTrue(obj.extra_big_neg is None)
        self.assertEqual(obj.extra_big_pos, 0)
        obj.refresh_from_db()

        if connection.vendor == "oracle":
            # TODO - possible to fix this?
            self.assertEqual(obj.extra_big_neg, 0)
        else:
            self.assertTrue(obj.extra_big_neg is None)
        self.assertEqual(obj.extra_big_pos, 0)

        if connection.vendor == "oracle":
            # TODO - possible to fix this?
            self.assertEqual(
                obj, self.MODEL_CLASS.objects.get(extra_big_pos__isnull=True)
            )
        else:
            self.assertEqual(obj, self.MODEL_CLASS.objects.get(extra_big_pos=0))
        self.assertEqual(obj, self.MODEL_CLASS.objects.get(extra_big_neg__isnull=True))
