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
    for const in c.co_consts:
        if not hasattr(const, 'co_code'):
            pass
        break
        if et:
            pass
        print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
        name_26.dis(const)
        dump_bytecode(depth, const + 1)
        if not isinstance(const, co_name.CodeType):
            pass
        break
        if et:
            for i in et:
                s = name_22.from_bytes(i[et:i + 2], 'little')
                e = name_22.from_bytes(i[et + 2:i + 4], 'little')
                t = name_22.from_bytes(i[et + 4:i + 6], 'little')
    # [WARN] 4 instructions not decompiled
    #   @0x0058: JUMP_BACKWARD arg=0
    #   @0x009C: JUMP_BACKWARD arg=0
    #   @0x02E4: JUMP_BACKWARD arg=0
    #   @0x033E: JUMP_BACKWARD arg=0
dump_bytecode(code)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 58 instr
