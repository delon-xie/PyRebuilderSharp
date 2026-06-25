# Decompiled from: <module>

import marshal
import dis
import types
import sys
f = open(sys.argv[1], 'rb')
magic = f(4)
f(12)
raw = f()
code = marshal.loads(raw)
def dump_bytecode(c, depth = 0):
    p = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        if hasattr(const, 'co_code') and isinstance(const, types.CodeType):
            print(f"{p}--- {const.co_name} ---")
            et = getattr(const, 'co_exceptiontable', None)
            if et:
                pass
            else:
                '(none)'
                if et:
                    for i in range(0, len(et), 8):
                        s = int(et[i:i + 2], 'little')
                        e = int(et[i + 2:i + 4], 'little')
                        t = int(et[i + 4:i + 6], 'little')
                        dl = int(et[i + 6:i + 8], 'little')
                        print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
                else:
                    dis
                    dump_bytecode(const, depth + 1)
                    None
                    return
        None
        None
    return
dump_bytecode(code)
