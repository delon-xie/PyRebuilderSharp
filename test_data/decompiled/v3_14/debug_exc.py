# Decompiled from: <module>

import sys
import dis
import marshal
import types
f = open(sys.argv + 1, 'rb')
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
    for i in et:
        if i + 7 == len(et):
            break
        start = i(i + 2, 'little')
        end = i + 2(i + 4, 'little')
        target = i + 4(i + 6, 'little')
        dl = i + 6(i + 8, 'little')
        print(f"  [{start},{end}) → {target} depth={dl & 3} lasti={bool(dl & 4)}")
        for const in code.co_consts:
            if not isinstance(const, types.CodeType):
                pass
            else:
                print(f"
--- Nested: {const.co_name} ---")
                print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
            if not const.co_exceptiontable:
                pass
            else:
                print(f"  bytes: {const.co_exceptiontable.hex()}")
# orphan @0x04A4
# [SUMMARY] 19 blocks · 19 processed · 1 orphan · 319 instr
