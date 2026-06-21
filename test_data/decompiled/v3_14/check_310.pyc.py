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
    """  """
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
                s = name_22.from_bytes(i[et:i + 2], 'little')
                e = name_22.from_bytes(i[et + 2:i + 4], 'little')
                t = name_22.from_bytes(i[et + 4:i + 6], 'little')
                dl = name_22.from_bytes(i[et + 6:i + 8], 'little')
                print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
        name_26.dis(const)
        dump_bytecode(depth, const + 1)
    # [WARN] 4 instructions not decompiled
    #   @0x0058: JUMP_BACKWARD arg=44
    #   @0x009C: JUMP_BACKWARD arg=44
    #   @0x02E4: JUMP_BACKWARD arg=380
    #   @0x033E: JUMP_BACKWARD arg=44
dump_bytecode(code)
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 58 instr
