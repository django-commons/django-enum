from enum import Enum
from django.db.models import Model
from django_enum import EnumField


class HashEquivalencyExample(Model):
    """
    This example model defines three enum fields. The first uses an enum that
    is not hash equivalent to its values. The second two are.
    """

    class NotHashEq(Enum):
        """
        Enums that inherit only from :class:`~enum.Enum` are not hash equivalent
        to their values by default.
        """

        VALUE1 = "V1"
        VALUE2 = "V2"
        VALUE3 = "V3"

    class HashEq(Enum):
        """
        We can force our Enum to be hash equivalent by overriding the necessary
        dunder methods..
        """

        VALUE1 = "V1"
        VALUE2 = "V2"
        VALUE3 = "V3"

        def __hash__(self):
            return hash(self.value)

        def __eq__(self, value) -> bool:
            if isinstance(value, self.__class__):
                return self.value == value.value
            try:
                return self.value == self.__class__(value).value
            except (ValueError, TypeError):
                return False

    class HashEqStr(str, Enum):  # or StrEnum on py 3.11+
        """
        Or we can inherit from the primitive value type.
        """

        VALUE1 = "V1"
        VALUE2 = "V2"
        VALUE3 = "V3"


    not_hash_eq = EnumField(NotHashEq)
    hash_eq = EnumField(HashEq)
    hash_eq_str = EnumField(HashEqStr)
