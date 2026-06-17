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
            pass
        else:
            break
        print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
        break
        break
        if not True:
            pass
        else:
            break
        for i in et:
            pass
dump_bytecode(code)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 57 instr
