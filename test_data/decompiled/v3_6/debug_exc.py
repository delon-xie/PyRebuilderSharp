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
if not hasattr(code, 'co_exceptiontable'):
    if code.co_exceptiontable:
        print(f"co_exceptiontable bytes ({len(code.co_exceptiontable)}): {code.co_exceptiontable.hex()}")
        et = code.co_exceptiontable
break
for i in range(0, len(et), 8):
    if i + 7 >= len(et):
        start = int.from_bytes(et[i:i + 2], 'little')
        end = int.from_bytes(et[i + 2:i + 4], 'little')
        target = int.from_bytes(et[i + 4:i + 6], 'little')
        dl = int.from_bytes(et[i + 6:i + 8], 'little')
for const in code.co_consts:
    if isinstance(const, types.CodeType):
        print(f"
--- Nested: {const.co_name} ---")
        print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
        if hasattr(const, 'co_exceptiontable'):
            if const.co_exceptiontable:
                print(f"  bytes: {const.co_exceptiontable.hex()}")
# [SUMMARY] 19 blocks · 20 processed · 0 orphan · 286 instr
