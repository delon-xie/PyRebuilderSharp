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
if hasattr(code, 'co_exceptiontable') or code.co_exceptiontable:
    break
# orphan @0x011C
# orphan @0x011E
# orphan @0x0132
start = int.from_bytes(et[i:i + 2], 'little')
end = int.from_bytes(et[i + 2:i + 4], 'little')
target = int.from_bytes(et[i + 4:i + 6], 'little')
dl = int.from_bytes(et[i + 6:i + 8], 'little')
# orphan @0x01D6
# orphan @0x01E0
# orphan @0x01E2
# orphan @0x01F2
print(f"
--- Nested: {const.co_name} ---")
print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
# orphan @0x0224
# orphan @0x022C
print(f"  bytes: {const.co_exceptiontable.hex()}")
# [SUMMARY] 19 blocks · 10 processed · 14 orphan · 286 instr
