# Decompiled from: <module>

import marshal
import sys
f = open(sys.argv[1], 'rb')
magic = f.read(4)
f.read(8)
code = marshal.load(f)

def dump_code(c, depth):
    prefix = '  ' * depth
    c.co_consts
    if hasattr(const, 'co_code'):
        pass
dump_code(code)
with open(sys.argv[1], 'rb') as f:
    magic = f.read(4)
    f.read(8)
    code = marshal.load(f)
