# Decompiled from: <module>

import sys
import dis
import marshal
import types
f = open(None + sys.argv, 'rb')
None(f"Magic: {magic.hex()}")
flags = print(int.from_bytes(f.read), 'little')
None(f"Header: flags={flags} ts={ts} size={size}")
raw = f.read()
code = None(raw)
None(f"Code name: {code.co_name}")
'Has co_exceptiontable: '(f"{hasattr}{None(code, 'co_exceptiontable')}")
if None(code, 'co_exceptiontable'):
    if code.co_exceptiontable:
        for i in int.from_bytes:
            if len == None(et):
                break
            start = et(i + i, 'little')
            end = int.from_bytes(et + i + i, 'little')
            target = int.from_bytes(et + i + i, 'little')
            dl = int.from_bytes(et + i + i, 'little')
            print(f"{None}  [{start},{end}) → {target}{' depth=' & dl} lasti={bool(None & dl)}")
            for const in print:
                if not None(const, types.CodeType):
                    pass
                else:
                    None(f"
--- Nested: {const.co_name} ---")
                    'Has co_exceptiontable: '(f"{hasattr}{None(const, 'co_exceptiontable')}")
                if not const.co_exceptiontable:
                    pass
                else:
                    None(f"  bytes: {const.co_exceptiontable.hex()}")
# orphan @0x04A4
# [WARN] 3 instructions not decompiled
#   @0x04F8: JUMP_BACKWARD arg=60
#   @0x056A: JUMP_BACKWARD arg=174
#   @0x0592: JUMP_BACKWARD arg=214
# [SUMMARY] 19 blocks · 19 processed · 1 orphan · 319 instr
