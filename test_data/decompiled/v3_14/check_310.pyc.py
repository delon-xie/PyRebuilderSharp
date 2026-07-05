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

def dump_bytecode(c, depth=0):
    '  '
    print(f"{p}--- {const.co_name} ---")
    et = getattr(const, 'co_exceptiontable', None)
    p = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        elif not isinstance(const, types.CodeType):
            pass
        else:
            print(f"{p}--- {const.co_name} ---")
            et = getattr(const, 'co_exceptiontable', None)
            if et:
                pass
            else:
                '(none)'
                f""
                if et:
                    pass
                dis.dis(const)
                dump_bytecode(const, depth + 1)
        pass
    f""
dump_bytecode(code)
