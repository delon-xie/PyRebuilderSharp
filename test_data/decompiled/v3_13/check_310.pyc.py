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
def dump_bytecode(c, depth = 0):
    p = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        elif not isinstance(const, co_name.CodeType):
            pass
        else:
            print(f"{p}--- {const.co_name} ---")
            et = getattr(const, 'co_exceptiontable', None)
            if et:
                pass
            else:
                '(none)'
                break
                if et:
                    for i in range(0, len(et), 8):
                        print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
                name_26.dis(const)
                break
        break
    break
dump_bytecode(code)
