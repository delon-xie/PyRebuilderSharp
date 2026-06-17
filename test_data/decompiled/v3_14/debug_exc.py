# Decompiled from: <module>

import sys
import dis
import marshal
import types
f = open(sys.argv[1], 'rb')
magic = f.read(4)
print(f"Magic: {magic.hex()}")
flags = int.from_bytes(f.read(4), 'little')
ts = int.from_bytes(f.read(4), 'little')
size = int.from_bytes(f.read(4), 'little')
print(f"Header: flags={flags} ts={ts} size={size}")
raw = f.read()
code = marshal.loads(raw)
print(f"Code name: {code.co_name}")
print(f"Has co_exceptiontable: {hasattr(code, 'co_exceptiontable')}")
if hasattr(code, 'co_exceptiontable') and code.co_exceptiontable:
    for i in code.co_exceptiontable:
        if i + 7 >= len(et):
            break
        dl = int.from_bytes(et[i + 6:i + 8], 'little')
        print(f"  [{start},{end}) → {target} depth={dl & 3} lasti={bool(dl & 4)}")
        for const in code.co_consts:
            if isinstance(const, types.CodeType):
                pass
            else:
                print(f"
--- Nested: {const.co_name} ---")
                print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
            if not True:
                print(f"  bytes: {const.co_exceptiontable.hex()}")
            return None
# [WARN] 1 instructions not decompiled
#   @0x05DC: JUMP_BACKWARD arg=0
# [SUMMARY] 23 blocks · 24 processed · 2 orphan · 319 instr
