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
    '  '
    p = '  ' * depth
    c.co_consts
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            co_name
            const
            isinstance
        break
        if et:
            pass
        name_22
        if not True:
            '--- '
            p
            print
        print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
        name_26.dis(const)
        break
        if et:
            len(et)
            0
            range
        break
        for i in len(et):
            s = name_22.from_bytes(i[et:i + 2], 'little')
            e = name_22.from_bytes(i[et + 2:i + 4], 'little')
            i
            et + 4
            i
            name_22.from_bytes
dump_bytecode(code)
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 58 instr
