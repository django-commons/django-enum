"""
Specialized has_any and has_all query lookups for flag enumerations.
"""

# from django.core.exceptions import FieldError
from django.db.models.lookups import Lookup

# from django_enum.utils import get_set_bits


class HasAllFlagsLookup(Lookup):
    """
    Query whether the left-hand side has all the bit flags on the right-hand
    side. This lookup bitwise ANDs the left-hand side with the right-hand side
    and checks that the result is equal to the right-hand side.
    """

    lookup_name = "has_all"

    def as_sql(self, compiler, connection):
        lhs_sql, lhs_params = self.process_lhs(compiler, connection)
        rhs_sql, rhs_params = self.process_rhs(compiler, connection)
        return (
            f"BITAND({lhs_sql}, {rhs_sql}) = {rhs_sql}"
            if connection.vendor == "oracle"
            else f"{lhs_sql} & {rhs_sql} = {rhs_sql}"
        ), [*lhs_params, *rhs_params, *rhs_params]


# class ExtraBigFlagMixin:
#
#     def get_prep_lookup(self):
#         return self.lhs.output_field.to_python(super().get_prep_lookup())
#
#     def get_rhs_op(self, connection, rhs):
#         if connection.vendor == 'postgresql':
#             return connection.operators['exact'] % '1'
#         raise FieldError(
#             f'{connection.vendor} does not support {self.lookup_name} on '
#             f'ExtraBigIntegerFlagFields.'
#         )


# class HasAllFlagsExtraBigLookup(
#     ExtraBigFlagMixin,
#     HasAllFlagsLookup
# ):
#     """
#     Support for bitwise has_all lookup on extra big integers (>64 bits)
#     stored as binary columns.
#
#     get_bit(, 0) AND get_bit(, 7) = 1;
#     """
#
#     def process_lhs(self, compiler, connection, lhs=None):
#         lhs_sql, lhs_params = Exact.process_lhs(
#               self,
#               compiler,
#               connection,
#               lhs
#         )
#         rhs_sql, rhs_params = Exact.process_rhs(self, compiler, connection)
#         bits = get_set_bits(rhs_params[0])
#         if self.rhs:
#             ret = ' AND '.join(
#                 [
#                     f'get_bit({lhs_sql}, %s)' for _ in range(len(bits))
#                 ]
#             ), bits
#             print(ret)
#             return ret
#         return lhs_sql, lhs_params


class HasAnyFlagsLookup(Lookup):
    """
    Query whether the left-hand side has any of the bit flags on the right-hand
    side. This lookup bitwise ANDs the left-hand side with the right-hand side
    and checks that the result is not equal to zero.
    """

    lookup_name = "has_any"

    def as_sql(self, compiler, connection):
        lhs_sql, lhs_params = self.process_lhs(compiler, connection)
        rhs_sql, rhs_params = self.process_rhs(compiler, connection)
        return (
            f"BITAND({lhs_sql}, {rhs_sql}) <> 0"
            if connection.vendor == "oracle"
            else f"{lhs_sql} & {rhs_sql} <> 0"
        ), [*lhs_params, *rhs_params]


# class HasAnyFlagsExtraBigLookup(
#     ExtraBigFlagMixin,
#     HasAnyFlagsLookup
# ):
#     """
#     Support for bitwise has_any lookup on extra big integers (>64 bits)
#     stored as binary columns.
#     """
#
#     def process_lhs(self, compiler, connection, lhs=None):
#         lhs_sql, lhs_params = Exact.process_lhs(
#               self,
#               compiler,
#               connection,
#               lhs
#         )
#         rhs_sql, rhs_params = Exact.process_rhs(self, compiler, connection)
#         bits = get_set_bits(rhs_params[0])
#         if self.rhs:
#             ret = ' OR '.join(
#                 [
#                     f'get_bit({lhs_sql}, %s)' for _ in range(len(bits))
#                 ]
#             ), [*bits, 1]
#             print(ret)
#             return ret
#         return lhs_sql, lhs_params
#
#     def process_rhs(self, compiler, connection):
#         rhs_sql, rhs_params = Exact.process_rhs(self, compiler, connection)
#         rhs_params[0] = 0
#         return rhs_sql, rhs_params
