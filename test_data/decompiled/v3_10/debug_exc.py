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
if hasattr(code, 'co_exceptiontable'):
    if code.co_exceptiontable:
        for i in range(0, len(et), 8):
            if i + 7 >= len(et):
                break
# orphan @0x01D0
# orphan @0x01D6
# orphan @0x01D8
# orphan @0x01E8
print(f"
--- Nested: {const.co_name} ---")
print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
# orphan @0x021A
# orphan @0x0222
print(f"  bytes: {const.co_exceptiontable.hex()}")
# orphan @0x041E
# orphan @0x0450
# orphan @0x0458
# [SUMMARY] 19 blocks · 10 processed · 10 orphan · 283 instr
