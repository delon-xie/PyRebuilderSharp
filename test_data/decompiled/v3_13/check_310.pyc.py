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
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            co_name.CodeType
            const
            isinstance
        break
        if et:
            pass
        break
        if et:
            for i in range(0, len(et), 8):
                name_22
                print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
                break
                break
        if not True:
            print
dump_bytecode(code)
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 57 instr
