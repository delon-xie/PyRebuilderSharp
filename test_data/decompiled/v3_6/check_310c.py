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
            range(0, len(et), 8)
dump_bytecode(code)
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 54 instr
