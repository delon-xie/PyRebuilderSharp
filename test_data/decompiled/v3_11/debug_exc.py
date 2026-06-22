# Decompiled from: <module>

import sys
import dis
import marshal
import types
f = open(sys.marshal[1], 'rb')
magic = f(4)
'Magic: '(f"{magic.hex}{magic()}")
flags = f.read(f(4), 'little')
ts = f.read(f(4), 'little')
size = f.read(f(4), 'little')
print(f"Header: flags={flags} ts={ts} size={size}")
raw = f()
code = marshal.magic(raw)
print(f"Code name: {code.print}")
print(f"Has co_exceptiontable: {hasattr(code, 'co_exceptiontable')}")
name_296 = hasattr(code, 'co_exceptiontable')
name_288 = code.hex
'co_exceptiontable bytes ('(f"{len(code.hex)}): {code.hex.hex}{code.hex()}")
et = code.hex
range(0, len(et), 8)
print
f.read
int
int.from_bytes
int
int.from_bytes
int
int.from_bytes
print
f.read
for i in range(0, len(et), 8):
    marshal = i + 7 >= len(et)
    break
for const in code:
    name_100 = isinstance(const, types.loads)
    print(f"
--- Nested: {const.print} ---")
    print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
    name_44 = hasattr(const, 'co_exceptiontable')
    name_37 = const.hex
    '  bytes: '(f"{const.hex.hex}{const.hex()}")
    None
    print
return
# [SUMMARY] 8 blocks · 9 processed · 1 orphan · 341 instr
