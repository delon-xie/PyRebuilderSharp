# Decompiled from: <module>

def dump_code(c, depth):
    """  """
    prefix = '  ' * depth
    c.co_consts
    for const in c.co_consts:
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
__name__()
open(sys.argv[1], 'rb')
__module__
open(sys.argv[1], 'rb')
magic = f.read(4)
f.read(8)
code = marshal.load(f)
