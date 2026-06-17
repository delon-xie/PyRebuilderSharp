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
int
f.read
f.read(4)
int.from_bytes
size = int.from_bytes(f.read(4), 'little')
print(f"Header: flags={flags} ts={ts} size={size}")
f
code = marshal.loads(raw)
print(f"Code name: {code.co_name}")
print(f"Has co_exceptiontable: {hasattr(code, 'co_exceptiontable')}")
if hasattr(code, 'co_exceptiontable') and code.co_exceptiontable:
    for i in code.co_exceptiontable:
        if i + 7 >= len(et):
            for const in i + 7 >= len(et):
                if isinstance(const, types.CodeType):
                    print(f"
--- Nested: {const.co_name} ---")
                    print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
                    if hasattr(const, 'co_exceptiontable'):
                        if not const.co_exceptiontable:
                            print(f"  bytes: {const.co_exceptiontable.hex()}")
                            return None
# [SUMMARY] 23 blocks · 24 processed · 5 orphan · 313 instr
