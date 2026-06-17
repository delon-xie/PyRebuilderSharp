def _is_single_bit(num):
    if num == 0:
        return False
    return num & (num - 1) == 0
