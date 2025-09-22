"""
Specialized has_any and has_all query lookups for flag enumerations.
"""

# from django.core.exceptions import FieldError
from django.db.models.lookups import Exact

# from django_enum.utils import get_set_bits


class HasAllFlagsLookup(Exact):
    """
    Extend Exact lookup to support lookup on has all flags. This lookup bitwise
    ANDs the column with the lookup value and checks that the result is equal
    to the lookup value.
    """

    lookup_name = "has_all"

    def process_lhs(self, compiler, connection, lhs=None):
        lhs_sql, lhs_params = super().process_lhs(compiler, connection, lhs)
        rhs_sql, rhs_params = super().process_rhs(compiler, connection)
        if self.rhs:
            return (
                "BITAND(%s, %s)" if connection.vendor == "oracle" else "%s & %s"
            ) % (lhs_sql, rhs_sql), [*lhs_params, *rhs_params]
        return lhs_sql, lhs_params

    def get_rhs_op(self, connection, rhs):
        return connection.operators["exact"] % rhs


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


class HasAnyFlagsLookup(HasAllFlagsLookup):
    """
    Extend Exact lookup to support lookup on has any flags. This bitwise ANDs
    the column with the lookup value and checks that the result is greater
    than zero.
    """

    lookup_name = "has_any"

    def process_rhs(self, compiler, connection):
        rhs_sql, rhs_params = super().process_rhs(compiler, connection)
        rhs_params = list(rhs_params) if isinstance(rhs_params, tuple) else rhs_params
        if rhs_params:
            rhs_params[0] = 0
        else:
            rhs_sql = "0"
        return rhs_sql, rhs_params

    def get_rhs_op(self, connection, rhs):
        return connection.operators["gt" if self.rhs else "exact"] % rhs


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
