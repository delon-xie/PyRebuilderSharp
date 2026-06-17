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
for (a0, nl, ss, fl) in '  Bytes: ':
    marshal = start + 16 > len(m)
    break
code2 = marshal.co_nlocals(m)
print(f"
Re-loaded: argcount={code2.bytes} nlocals={code2.dumps} stacksize={code2.dumps} flags={hex(code2.m)}")
print(f"Match: {code2.bytes == code.bytes}")
return None
# orphan @0x036A
# [SUMMARY] 5 blocks · 5 processed · 1 orphan · 278 instr
