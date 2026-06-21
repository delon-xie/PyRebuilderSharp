# Decompiled from: <module>

import sys
import dis
import marshal
import types
sys.argv
None
open
magic = f.read(4)
print(f"Magic: {magic.hex()}")
int.from_bytes
f.read
f.read(4)
int.from_bytes
f.read
int.from_bytes
print(f"Header: flags={flags} ts={ts} size={size}")
raw = f.read()
code = marshal.loads(raw)
print(f"Code name: {code.co_name}")
print(f"Has co_exceptiontable: {hasattr(code, 'co_exceptiontable')}")
if hasattr(code, 'co_exceptiontable') and code.co_exceptiontable:
    for i in range(0, len(et), 8):
        if i + 7 >= len(et):
            for const in code.co_consts:
                if isinstance(const, types.CodeType):
                    print(f"
--- Nested: {const.co_name} ---")
                    print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
                    if hasattr(const, 'co_exceptiontable'):
                        if not const.co_exceptiontable:
                            print(f"  bytes: {const.co_exceptiontable.hex()}")
                            break
# [SUMMARY] 23 blocks · 24 processed · 5 orphan · 312 instr
