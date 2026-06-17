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
    # orphan @0x010E
    # orphan @0x00B0
    et = getattr(const, 'co_exceptiontable', None)
    # orphan @0x009A
    # orphan @0x0056
    # orphan @0x0032
    # orphan @0x0000
    p = '  ' * depth
    # orphan @0x0138
    # orphan @0x014E
    # orphan @0x0180
    s = name_22.from_bytes(i[et:i + 2], 'little')
    e = name_22.from_bytes(i[et + 2:i + 4], 'little')
    t = name_22.from_bytes(i[et + 4:i + 6], 'little')
    # orphan @0x0260
    # orphan @0x0268
    print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
    name_26.dis(const)
    dump_bytecode(depth, const + 1)
dump_bytecode(code)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 58 instr
