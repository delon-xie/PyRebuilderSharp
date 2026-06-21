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
    for i in range(0, len(et), 8):
        if i + 7 >= len(et):
            break
        else:
            start = int.from_bytes(et[i:i + 2], 'little')
            end = int.from_bytes(et[i + 2:i + 4], 'little')
            target = int.from_bytes(et[i + 4:i + 6], 'little')
            dl = int.from_bytes(et[i + 6:i + 8], 'little')
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
        break
# orphan @0x0444
# [SUMMARY] 18 blocks · 18 processed · 1 orphan · 312 instr
