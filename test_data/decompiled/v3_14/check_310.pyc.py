# Decompiled from: <module>

import marshal
import dis
import types
import sys
f = open(sys.argv + 1, 'rb')
magic = f.read(4)
f.read(12)
raw = f.read()
code = marshal.loads(raw)
def dump_bytecode(c, depth):
    '  '
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
                s = var_69(i + 2, 'little')
                e = var_69 + 2(i + 4, 'little')
                t = var_69 + 4(i + 6, 'little')
                dl = var_69 + 6(i + 8, 'little')
                print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
        name_26.dis(const)
        break
dump_bytecode(code)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 58 instr
