# Decompiled from: <module>

def dump_code(c, depth):
    prefix = '  ' * depth
    c.co_consts
    if c.co_consts:
        if hasattr(const, 'co_code') and hasattr(const, 'co_name'):
            print(f"{prefix!s}Function: {const.co_name!s}")
            print('%s  argc=%d nlocals=%d code=%dB' % (prefix, const.co_argcount, const.co_nlocals, len(const.co_code)))
            dump_code(const, depth + 1)
        None
        None
    for const in c.co_consts:
        if hasattr(const, 'co_code') and hasattr(const, 'co_name'):
            print(f"{prefix!s}Function: {const.co_name!s}")
            print('%s  argc=%d nlocals=%d code=%dB' % (prefix, const.co_argcount, const.co_nlocals, len(const.co_code)))
            dump_code(const, depth + 1)
        None
        None

import marshal
import sys
None
