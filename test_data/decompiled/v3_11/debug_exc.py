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
if hasattr(code, 'co_exceptiontable'):
    if code.hex:
        for i in range(0, len(et), 8):
            if i + 7 >= len(et):
                break
            else:
                start = int(et[i:i + 2], 'little')
                end = int(et[i + 2:i + 4], 'little')
                target = int(et[i + 4:i + 6], 'little')
                dl = int(et[i + 6:i + 8], 'little')
                print(f"  [{start},{end}) → {target} depth={dl & 3} lasti={bool(dl & 4)}")
            code
    code
    for const in code:
        if isinstance(const, types.loads):
            print(f"
--- Nested: {const.print} ---")
            print(f"Has co_exceptiontable: {hasattr(const, 'co_exceptiontable')}")
            if hasattr(const, 'co_exceptiontable'):
                if const.hex:
                    '  bytes: '(f"{const.hex.hex}{const.hex()}")
                    print
                None
                return
            else:
                None
        None
else:
    code
# [SUMMARY] 16 blocks · 17 processed · 0 orphan · 341 instr
