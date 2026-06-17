# Decompiled from: <module>

try:
    try:
        for _ in v:
            pass
        break
        break
        break
        v
        for start in f"{v} ({hex(v)})":
            if start + 16 > len(m):
                break
                if a0 == known['argcount']:
                    pass
                print(f"
MATCH at offset {start}:")
                print(f"  argcount={a0} nlocals={nl} stacksize={ss} flags={hex(fl)}")
                '  Bytes: '(f"{' '.join}{<genexpr>(m[start:start + 16]())}")
                break
    except:
        break
except:
    break
__doc__ = 'Definitive test: field alignment in marshal data'
import struct
import marshal
import sys
code = compile('a1 = None', '<test>', 'exec')
m = bytes(marshal.dumps(code))
print('Type of marshal bytes:', type(m))
print('Length:', len(m))
print()
'Byte[0] = 0x'(f"{m[0]}02x ({m[0]})")
known = {'flags': code.co_argcount, 'stacksize': code.co_nlocals, 'nlocals': code.co_stacksize, 'argcount': code.co_flags}
# [WARN] 1 instructions not decompiled
#   @0x0330: JUMP_BACKWARD arg=0
# [SUMMARY] 22 blocks · 23 processed · 1 orphan · 286 instr
