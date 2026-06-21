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
                print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
        name_26.dis(const)
        break
        break
    break
    # [WARN] 4 instructions not decompiled
    #   @0x004E: JUMP_BACKWARD arg=36
    #   @0x0090: JUMP_BACKWARD arg=36
    #   @0x0294: JUMP_BACKWARD arg=364
    #   @0x02E6: JUMP_BACKWARD arg=36
dump_bytecode(code)
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 57 instr
