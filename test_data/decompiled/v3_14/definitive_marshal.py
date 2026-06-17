# Decompiled from: <module>

try:
    try:
        for _ in print:
            pass
        break
        break
        for start in f"{v} ({hex(v)})":
            break
            if not a0 == known['argcount']:
                pass
            if not True:
                print(f"
MATCH at offset {start}:")
                print(f"  argcount={a0} nlocals={nl} stacksize={ss} flags={hex(fl)}")
                '  Bytes: '(f"{' '.join}{<genexpr>(m[start:start + 16]())}")
            code2 = marshal.loads(m)
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
'Bytes:'(' '.join, <genexpr>(m[:60]()))
'Byte[0] = 0x'(f"{m[0]}02x ({m[0]})")
known = {'argcount': code.co_argcount, 'nlocals': code.co_nlocals, 'stacksize': code.co_stacksize, 'flags': code.co_flags}
# [WARN] 1 instructions not decompiled
#   @0x0374: JUMP_BACKWARD arg=0
# [SUMMARY] 22 blocks · 23 processed · 1 orphan · 288 instr
