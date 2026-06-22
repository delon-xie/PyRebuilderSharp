# Decompiled from: <module>

import marshal
import dis
import types
import sys
f = open(sys.argv[1], 'rb')
magic = f.read(4)
f.read(12)
raw = f.read()
code = marshal.loads(raw)
def dump_bytecode(c, depth):
    p = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        break
        if et:
            pass
dump_bytecode(code)
