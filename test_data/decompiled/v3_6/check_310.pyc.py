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
    for const in c.co_consts:
        if hasattr(const, 'co_code') and et:
            pass
        dl = int.from_bytes(et[i + 6:i + 8], 'little')
        print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
        for i in range(0, len(et), 8):
            s = int.from_bytes(et[i:i + 2], 'little')
            e = int.from_bytes(et[i + 2:i + 4], 'little')
        dis.dis(const)
        dump_bytecode(const, depth + 1)
        break
        break
        if et:
            pass
dump_bytecode(code)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 54 instr
