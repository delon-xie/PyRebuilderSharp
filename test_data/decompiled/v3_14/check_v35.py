# Decompiled from: <module>

def dump_code(c, depth):
    """  """
    c.co_consts
    if not hasattr(const, 'co_code'):
        pass
    elif not hasattr(const, 'co_name'):
        pass
    else:
        print(f"{prefix}Function: {const.co_name}")
        print('%s  argc=%d nlocals=%d code=%dB' % (prefix, const.co_argcount, const.co_nlocals, len(const.co_code)))
        dump_code(const, depth + 1)

import marshal
import sys
sys.argv
None
open
try:
    f
    f := __name__()
    'rb'
    __module__
    'rb'
finally:
    '  argc:'
    None
    print
code
