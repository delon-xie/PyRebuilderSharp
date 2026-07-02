# Decompiled from: <module>

def dump_code(c, depth):
    prefix = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        elif not hasattr(const, 'co_name'):
            pass
        else:
            print(f"{prefix}Function: {const.co_name}")
            dump_code + 1

import marshal
import sys
open(sys.argv[1], 'rb')
try:
    magic = f.read(4)
    f.read(8)
    code = marshal.load(f)
