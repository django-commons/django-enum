from .models.equivalency import EquivalencyExample
from django.core.exceptions import ValidationError


EquivalencyExample.objects.create(txt_enum='V0', txt_choices='V0')

# txt_enum fields will always be an instance of the TextEnum type, unless
# set to a value that is not part of the enumeration

eq_ex = EquivalencyExample.objects.first()
assert eq_ex
assert isinstance(eq_ex.txt_enum, EquivalencyExample.TextEnum)
assert isinstance(eq_ex.txt_choices, str)

# by default EnumFields are more strict, this is possible:
EquivalencyExample.objects.create(txt_choices='AA')

# but this will throw a ValueError (unless strict=False)
try:
    EquivalencyExample.objects.create(txt_enum='AA')
    assert False
except ValueError:
    assert True

# and this will throw a ValidationError
try:
    EquivalencyExample(txt_enum='AA').full_clean()
    assert False
except ValidationError:
    assert True
