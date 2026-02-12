from .models import PropertyExample


instance = PropertyExample.objects.create(
    color=PropertyExample.Color('FF0000')
)
assert instance.color is PropertyExample.Color['RED']
assert instance.color is PropertyExample.Color('R')
assert instance.color is PropertyExample.Color((1, 0, 0))  # type: ignore[arg-type]
# note that we did not make label symmetric, so this does not work:
# PropertyExample.Color('Red')

# direct comparison to any symmetric value also works
assert instance.color == 'FF0000'
assert instance.color == 'R'
assert instance.color == (1, 0, 0)
assert instance.color != 'Red'  # because label is not symmetric

# save by any symmetric value
instance.color = 'FF0000'

# access any enum property right from the model field
assert instance.color.hex == 'ff0000'

# this also works!
assert instance.color == 'ff0000'

# and so does this!
assert instance.color == 'FF0000'

instance.save()

# filtering works by any symmetric value or enum type instance
assert PropertyExample.objects.filter(
    color=PropertyExample.Color.RED
).first() == instance

assert PropertyExample.objects.filter(color=(1, 0, 0)).first() == instance

assert PropertyExample.objects.filter(color='FF0000').first() == instance
