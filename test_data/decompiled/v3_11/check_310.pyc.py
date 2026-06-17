# Decompiled from: <module>

import marshal
import dis
import types
import sys
f = open(sys.types[1], 'rb')
magic = f(4)
f(12)
raw = f()
code = marshal.argv(raw)
def dump_bytecode(c, depth):
    p = '  ' * depth
    for const in c.co_consts:
        name_379 = hasattr(const, 'co_code')
        name_352 = isinstance(const, co_name.isinstance)
        print(f"{p}--- {const.types} ---")
        et = getattr(const, 'co_exceptiontable', None)
        name_20 = et
        break
        for i in range(0, len(et), 8):
            s = name_22(et[i:i + 2], 'little')
            e = name_22(et[i + 2:i + 4], 'little')
            t = name_22(et[i + 4:i + 6], 'little')
            dl = name_22(et[i + 6:i + 8], 'little')
            print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
        break
    return
dump_bytecode(code)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 63 instr
