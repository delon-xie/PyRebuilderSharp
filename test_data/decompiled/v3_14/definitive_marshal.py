# Decompiled from: <module>

try:
    try:
        for _ in print:
            pass
        break
        break
        for start in f"{v} ({hex(v)})":
            if start + 16 > len(m):
                break
                if a0 == known['argcount']:
                    pass
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
print()
'Byte[0] = 0x'(f"{m[0]}02x ({m[0]})")
known = {'argcount': code.co_argcount, 'nlocals': code.co_nlocals, 'stacksize': code.co_stacksize, 'flags': code.co_flags}
# [SUMMARY] 22 blocks · 23 processed · 5 orphan · 292 instr
