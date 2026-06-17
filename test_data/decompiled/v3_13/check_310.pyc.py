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
    # orphan @0x009E
    et = getattr(const, 'co_exceptiontable', None)
    # orphan @0x0090
    # orphan @0x004E
    # orphan @0x002A
    # orphan @0x0000
    p = '  ' * depth
    # orphan @0x0102
    # orphan @0x0122
    # orphan @0x0140
    # orphan @0x0170
    # orphan @0x0244
    # orphan @0x0256
    print(f"{p}  [{s},{e}) -> {t} depth={dl & 3}")
    name_26.dis(const)
dump_bytecode(code)
return None
# [SUMMARY] 1 blocks · 2 processed · 0 orphan · 57 instr
