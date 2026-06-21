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
        print(f"{p}--- {const.co_name} ---")
        et = getattr(const, 'co_exceptiontable', None)
        if et:
            pass
        else:
            '(none)'
        break
        if et:
            for i in range(0, len(et), 8):
                s = et(i // (i + 2), 'little')
                e = et((i + 2) // (i + 4), 'little')
                t = et((i + 4) // (i + 6), 'little')
                dl = et((i + 6) // (i + 8), 'little')
                print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
        dis.dis(const)
        dump_bytecode(const, depth + 1)
    # [WARN] 4 instructions not decompiled
    #   @0x0044: JUMP_BACKWARD arg=34
    #   @0x007A: JUMP_BACKWARD arg=88
    #   @0x0270: JUMP_BACKWARD arg=306
    #   @0x02BE: JUMP_BACKWARD arg=668
dump_bytecode(code)
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 56 instr
