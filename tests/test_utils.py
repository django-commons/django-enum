from django.test import TestCase
from django_enum.utils import get_set_bits, get_set_values, decompose, members
from importlib.util import find_spec
import pytest
import enum
import sys


class UtilsTests(TestCase):
    def test_get_set_values(self):
        from tests.djenum.enums import SmallPositiveFlagEnum

        self.assertEqual(
            get_set_values(None),
            [],
        )

        self.assertEqual(
            get_set_values(SmallPositiveFlagEnum.ONE | SmallPositiveFlagEnum.THREE),
            [SmallPositiveFlagEnum.ONE.value, SmallPositiveFlagEnum.THREE.value],
        )
        self.assertEqual(
            get_set_values(
                int((SmallPositiveFlagEnum.ONE | SmallPositiveFlagEnum.THREE).value)
            ),
            [SmallPositiveFlagEnum.ONE.value, SmallPositiveFlagEnum.THREE.value],
        )

        self.assertEqual(
            get_set_values(
                SmallPositiveFlagEnum.TWO | SmallPositiveFlagEnum.FIVE,
            ),
            [SmallPositiveFlagEnum.TWO.value, SmallPositiveFlagEnum.FIVE.value],
        )

        self.assertEqual(
            get_set_values(
                (
                    SmallPositiveFlagEnum.ONE
                    | SmallPositiveFlagEnum.TWO
                    | SmallPositiveFlagEnum.THREE
                    | SmallPositiveFlagEnum.FOUR
                    | SmallPositiveFlagEnum.FIVE
                ).value,
            ),
            [
                SmallPositiveFlagEnum.ONE.value,
                SmallPositiveFlagEnum.TWO.value,
                SmallPositiveFlagEnum.THREE.value,
                SmallPositiveFlagEnum.FOUR.value,
                SmallPositiveFlagEnum.FIVE.value,
            ],
        )

        self.assertEqual(
            get_set_values(SmallPositiveFlagEnum.FOUR),
            [SmallPositiveFlagEnum.FOUR.value],
        )

        self.assertEqual(get_set_values(SmallPositiveFlagEnum(0)), [])

        self.assertEqual(get_set_values(int(SmallPositiveFlagEnum(0))), [])

        self.assertEqual(get_set_values(0), [])

    def test_get_set_bits(self):
        from tests.djenum.enums import SmallPositiveFlagEnum

        self.assertEqual(
            get_set_bits(None),
            [],
        )

        self.assertEqual(
            get_set_bits(SmallPositiveFlagEnum.ONE | SmallPositiveFlagEnum.THREE),
            [10, 12],
        )
        self.assertEqual(
            get_set_bits(
                int((SmallPositiveFlagEnum.ONE | SmallPositiveFlagEnum.THREE).value)
            ),
            [10, 12],
        )

        self.assertEqual(
            get_set_bits(
                SmallPositiveFlagEnum.TWO | SmallPositiveFlagEnum.FIVE,
            ),
            [11, 14],
        )

        self.assertEqual(get_set_bits(SmallPositiveFlagEnum.FOUR), [13])

        self.assertEqual(get_set_bits(SmallPositiveFlagEnum(0)), [])

        self.assertEqual(get_set_bits(int(SmallPositiveFlagEnum(0))), [])

        self.assertEqual(get_set_bits(0), [])

    def test_decompose(self):
        from tests.djenum.enums import SmallPositiveFlagEnum

        self.assertEqual(decompose(None), [])

        self.assertEqual(
            decompose(SmallPositiveFlagEnum.ONE | SmallPositiveFlagEnum.THREE),
            [SmallPositiveFlagEnum.ONE, SmallPositiveFlagEnum.THREE],
        )

        self.assertEqual(
            decompose(
                SmallPositiveFlagEnum.TWO | SmallPositiveFlagEnum.FIVE,
            ),
            [SmallPositiveFlagEnum.TWO, SmallPositiveFlagEnum.FIVE],
        )

        self.assertEqual(
            decompose(SmallPositiveFlagEnum.FOUR), [SmallPositiveFlagEnum.FOUR]
        )

        self.assertEqual(decompose(SmallPositiveFlagEnum(0)), [])

        self.assertEqual(decompose(int(SmallPositiveFlagEnum(0))), [])

        self.assertEqual(decompose(0), [])

    def test_members(self):
        class NoAliasesEnum(enum.Enum):
            A = 1
            B = 2
            C = 3

        if sys.version_info[:2] >= (3, 11):

            class AliasesEnum(enum.Enum):
                A = 1
                B = 2
                C = 3
                D = A
                E = B

                @enum.nonmember
                def check(self):
                    return "check"

                @enum.member
                class NestedType:
                    pass

        else:

            class AliasesEnum(enum.Enum):
                A = 1
                B = 2
                C = 3
                D = A
                E = B

                @property
                def X(self):
                    return self.A

                class NestedType:
                    pass

        self.assertEqual(
            list(members(NoAliasesEnum)),
            [NoAliasesEnum.A, NoAliasesEnum.B, NoAliasesEnum.C],
        )

        self.assertEqual(
            list(members(NoAliasesEnum, aliases=False)),
            [NoAliasesEnum.A, NoAliasesEnum.B, NoAliasesEnum.C],
        )

        self.assertEqual(
            list(members(AliasesEnum, aliases=False)),
            [AliasesEnum.A, AliasesEnum.B, AliasesEnum.C, AliasesEnum.NestedType],
        )

        self.assertEqual(
            list(members(AliasesEnum)),
            [
                AliasesEnum.A,
                AliasesEnum.B,
                AliasesEnum.C,
                AliasesEnum.D,
                AliasesEnum.E,
                AliasesEnum.NestedType,
            ],
        )

        class NoAliasesFlag(enum.Flag):
            A = 1 << 0
            B = 1 << 1
            C = 1 << 2

            @property
            def not_a_member(self):
                return self.A | self.B | self.C

        class AliasesFlag(enum.Flag):
            A = 1 << 0
            B = 1 << 1
            C = 1 << 2
            AB = A | B
            BC = B | C
            ABC = A | B | C
            AA = A
            BB = B

            @property
            def not_a_member(self):
                return self.A | self.B | self.C

        self.assertEqual(
            list(members(NoAliasesFlag)),
            [NoAliasesFlag.A, NoAliasesFlag.B, NoAliasesFlag.C],
        )

        self.assertEqual(
            list(members(NoAliasesFlag, aliases=False)),
            [NoAliasesFlag.A, NoAliasesFlag.B, NoAliasesFlag.C],
        )

        self.assertEqual(
            list(members(AliasesFlag, aliases=False)),
            [AliasesFlag.A, AliasesFlag.B, AliasesFlag.C],
        )

        self.assertEqual(
            list(members(AliasesFlag)),
            [
                AliasesFlag.A,
                AliasesFlag.B,
                AliasesFlag.C,
                AliasesFlag.AB,
                AliasesFlag.BC,
                AliasesFlag.ABC,
                AliasesFlag.AA,
                AliasesFlag.BB,
            ],
        )

    @pytest.mark.skipif(
        find_spec("enum_properties") is None,
        reason="enum_properties not installed",
    )
    def test_members_props(self):
        import typing as t
        from enum_properties import (
            EnumProperties,
            IntFlagProperties,
            Symmetric,
            symmetric,
        )

        class NoAliasesEnum(EnumProperties):
            label: t.Annotated[str, Symmetric()]

            A = 1, "a"
            B = 2, "b"
            C = 3, "c"

            @symmetric(case_fold=True)
            def x3(self):
                return self.label * 3

        self.assertIs(NoAliasesEnum(NoAliasesEnum.A.x3), NoAliasesEnum.A)

        if sys.version_info[:2] >= (3, 11):

            class AliasesEnum(EnumProperties):
                label: t.Annotated[str, Symmetric()]

                A = 1, "a"
                B = 2, "b"
                C = 3, "c"
                D = A, "d"
                E = B, "e"

        else:

            class AliasesEnum(EnumProperties):
                label: t.Annotated[str, Symmetric()]

                A = 1, "a"
                B = 2, "b"
                C = 3, "c"
                D = A, "d"
                E = B, "e"

                @property
                def X(self):
                    return self.A

                class NestedType:
                    pass

        self.assertEqual(
            list(members(NoAliasesEnum)),
            [NoAliasesEnum.A, NoAliasesEnum.B, NoAliasesEnum.C],
        )

        self.assertEqual(
            list(members(NoAliasesEnum, aliases=False)),
            [NoAliasesEnum.A, NoAliasesEnum.B, NoAliasesEnum.C],
        )

        self.assertEqual(
            list(members(AliasesEnum, aliases=False)),
            [AliasesEnum.A, AliasesEnum.B, AliasesEnum.C],
        )

        self.assertEqual(
            list(members(AliasesEnum)),
            [AliasesEnum.A, AliasesEnum.B, AliasesEnum.C, AliasesEnum.D, AliasesEnum.E],
        )

        class NoAliasesFlag(IntFlagProperties):
            label: t.Annotated[str, Symmetric()]

            A = 1 << 0, "a"
            B = 1 << 1, "b"
            C = 1 << 2, "c"

            @property
            def not_a_member(self):
                return self.A | self.B | self.C

        class AliasesFlag(IntFlagProperties):
            label: t.Annotated[str, Symmetric()]

            A = 1 << 0, "a"
            B = 1 << 1, "b"
            C = 1 << 2, "c"

            AB = A | B, "ab"
            BC = B | C, "bc"
            ABC = A | B | C, "abc"

            AA = A, "aa"
            BB = B, "bb"

            @property
            def not_a_member(self):
                return self.A | self.B | self.C

        self.assertEqual(
            list(members(NoAliasesFlag)),
            [NoAliasesFlag.A, NoAliasesFlag.B, NoAliasesFlag.C],
        )

        self.assertEqual(
            list(members(NoAliasesFlag, aliases=False)),
            [NoAliasesFlag.A, NoAliasesFlag.B, NoAliasesFlag.C],
        )

        self.assertEqual(
            list(members(AliasesFlag, aliases=False)),
            [AliasesFlag.A, AliasesFlag.B, AliasesFlag.C],
        )

        self.assertEqual(
            list(members(AliasesFlag)),
            [
                AliasesFlag.A,
                AliasesFlag.B,
                AliasesFlag.C,
                AliasesFlag.AB,
                AliasesFlag.BC,
                AliasesFlag.ABC,
                AliasesFlag.AA,
                AliasesFlag.BB,
            ],
        )

    @pytest.mark.skipif(
        find_spec("enum_properties") is None,
        reason="enum_properties not installed",
    )
    def test_members_choices(self):
        import typing as t
        from enum_properties import symmetric
        from django_enum.choices import IntegerChoices, FlagChoices

        class NoAliasesEnum(IntegerChoices):
            A = 1, "a"
            B = 2, "b"
            C = 3, "c"

            @symmetric(case_fold=True)
            def x3(self):
                return self.label * 3

        self.assertIs(NoAliasesEnum(NoAliasesEnum.A.x3), NoAliasesEnum.A)

        self.assertEqual(
            list(members(NoAliasesEnum)),
            [NoAliasesEnum.A, NoAliasesEnum.B, NoAliasesEnum.C],
        )

        self.assertEqual(
            list(members(NoAliasesEnum, aliases=False)),
            [NoAliasesEnum.A, NoAliasesEnum.B, NoAliasesEnum.C],
        )

        # choices types disallow duplicates
        class AliasesEnum(IntegerChoices):
            A = 1, "a"
            B = 2, "b"
            C = 3, "c"

        self.assertEqual(
            list(members(AliasesEnum, aliases=False)),
            [AliasesEnum.A, AliasesEnum.B, AliasesEnum.C],
        )

        self.assertEqual(
            list(members(AliasesEnum)),
            [
                AliasesEnum.A,
                AliasesEnum.B,
                AliasesEnum.C,
            ],
        )

        class NoAliasesFlag(FlagChoices):
            A = 1 << 0, "a"
            B = 1 << 1, "b"
            C = 1 << 2, "c"

            @property
            def not_a_member(self):
                return self.A | self.B | self.C

        class AliasesFlag(FlagChoices):
            A = 1 << 0, "a"
            B = 1 << 1, "b"
            C = 1 << 2, "c"

            if sys.version_info[:2] >= (3, 14):
                AB = A | B, "ab"
                BC = B | C, "bc"
                ABC = A | B | C, "abc"
            else:
                AB = A[0] | B[0], "ab"
                BC = B[0] | C[0], "bc"
                ABC = A[0] | B[0] | C[0], "abc"

            @property
            def not_a_member(self):
                return self.A | self.B | self.C

        self.assertEqual(
            list(members(NoAliasesFlag)),
            [NoAliasesFlag.A, NoAliasesFlag.B, NoAliasesFlag.C],
        )

        self.assertEqual(
            list(members(NoAliasesFlag, aliases=False)),
            [NoAliasesFlag.A, NoAliasesFlag.B, NoAliasesFlag.C],
        )

        self.assertEqual(
            list(members(AliasesFlag, aliases=False)),
            [AliasesFlag.A, AliasesFlag.B, AliasesFlag.C],
        )

        self.assertEqual(
            list(members(AliasesFlag)),
            [
                AliasesFlag.A,
                AliasesFlag.B,
                AliasesFlag.C,
                AliasesFlag.AB,
                AliasesFlag.BC,
                AliasesFlag.ABC,
            ],
        )

        class AliasesFlagWithProp(FlagChoices):
            prop: bool

            A = 1 << 0, "a", False
            B = 1 << 1, "b", False
            C = 1 << 2, "c", False

            if sys.version_info[:2] >= (3, 14):
                AB = A | B, "ab", True
                BC = B | C, "bc", True
                ABC = A | B | C, "abc", True
            else:
                AB = A[0] | B[0], "ab", True
                BC = B[0] | C[0], "bc", True
                ABC = A[0] | B[0] | C[0], "abc", True

            @property
            def not_a_member(self):
                return self.A | self.B | self.C

        self.assertEqual(
            list(members(AliasesFlagWithProp, aliases=False)),
            [AliasesFlagWithProp.A, AliasesFlagWithProp.B, AliasesFlagWithProp.C],
        )

        self.assertEqual(
            list(members(AliasesFlagWithProp)),
            [
                AliasesFlagWithProp.A,
                AliasesFlagWithProp.B,
                AliasesFlagWithProp.C,
                AliasesFlagWithProp.AB,
                AliasesFlagWithProp.BC,
                AliasesFlagWithProp.ABC,
            ],
        )
