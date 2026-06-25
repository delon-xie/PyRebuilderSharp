def _gt_from_lt(self, other):
    """Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and self != other


def _is_dunder(name):
    """Returns True if a __dunder__ name, False otherwise."""
    return (
        len(name) > 4 and
        name[:2] == name[-2:] == '__' and
        name[2] != '_' and
        name[-3] != '_'
    )


def _is_single_bit(num):
    """Test if num is a power of 2."""
    if num == 0:
        return False
    num &= num - 1
    return num == 0
