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
        if not hasattr(const, 'co_code'):
            pass
        print(f"{p}--- {const.co_name} ---")
        et = getattr(const, 'co_exceptiontable', None)
        if et:
            pass
        break
        if et:
            for i in name_22.from_bytes:
                s = et(i // (i + 2), 'little')
                e = et((i + 2) // (i + 4), 'little')
                t = et((i + 4) // (i + 6), 'little')
                dl = et((i + 6) // (i + 8), 'little')
                print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
        dis.dis(const)
        dump_bytecode(const, depth + 1)
dump_bytecode(code)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 56 instr
