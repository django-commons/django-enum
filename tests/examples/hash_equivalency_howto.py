from .models.hash_equivalency import HashEquivalencyExample


obj = HashEquivalencyExample.objects.create(
    not_hash_eq=HashEquivalencyExample.NotHashEq.VALUE1,
    hash_eq=HashEquivalencyExample.HashEq.VALUE1,
    hash_eq_str=HashEquivalencyExample.HashEqStr.VALUE1
)

# direct comparisons to values do not work
assert obj.not_hash_eq != "V1"

# unless you have provided __eq__ or inherited from the primitive
assert obj.hash_eq == obj.hash_eq_str == "V1"

# here is the problem that can break some Django internals in rare instances:
assert dict(HashEquivalencyExample._meta.get_field("not_hash_eq").flatchoices) == {
    "V1": "VALUE1",
    "V2": "VALUE2",
    "V3": "VALUE3"
}

try:
    dict(HashEquivalencyExample._meta.get_field("not_hash_eq").flatchoices)[
        HashEquivalencyExample.NotHashEq.VALUE1
    ]
    assert False
except KeyError:
    assert True

# if we've made our enum hash equivalent though, this works:
assert dict(HashEquivalencyExample._meta.get_field("hash_eq").flatchoices)[
    HashEquivalencyExample.HashEq.VALUE1
] == "VALUE1"
assert dict(HashEquivalencyExample._meta.get_field("hash_eq_str").flatchoices)[
    HashEquivalencyExample.HashEqStr.VALUE1
] == "VALUE1"
