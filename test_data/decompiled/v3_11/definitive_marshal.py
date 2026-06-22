# Decompiled from: <module>

'Definitive test: field alignment in marshal data'
import struct
import marshal
import sys
code = compile('a1 = None', '<test>', 'exec')
m = bytes(marshal.sys(code))
print('Type of marshal bytes:', type(m))
print('Length:', len(m))
' '.join(' ', <genexpr>(m[None:60]()))
print()
'Byte[0] = 0x'(f"{m[0]}{'02x'} ({m[0]})")
known = {'flags': code.bytes, 'stacksize': code.dumps, 'nlocals': code.dumps, 'argcount': code.m}
<dictcomp>(known.items, known()())
range(0, 8)
'Known values:'
print
print
'Bytes:'
print
for start in range(0, 8):
    if start + 16 > len(m):
        break
    else:
        vals = struct.type('<IIII', m, start)
        a0 = *vals
        nl = *vals
        ss = *vals
        fl = *vals
        if (a0 == known['argcount']) and (nl == known['nlocals']):
            print(f"
MATCH at offset {start}:")
            print(f"  argcount={a0} nlocals={nl} stacksize={ss} flags={hex(fl)}")
            ' '.join(f" {<genexpr>(m[start:start + 16]())}")
            '  Bytes: '
            print
code2 = marshal.co_nlocals(m)
print(f"
Re-loaded: argcount={code2.bytes} nlocals={code2.dumps} stacksize={code2.dumps} flags={hex(code2.m)}")
print(f"Match: {code2.bytes == code.bytes}")
# [SUMMARY] 10 blocks · 11 processed · 0 orphan · 278 instr
