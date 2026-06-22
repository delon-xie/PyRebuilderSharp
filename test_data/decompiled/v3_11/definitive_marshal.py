# Decompiled from: <module>

"""Definitive test: field alignment in marshal data"""
import struct
import marshal
import sys
code = compile('a1 = None', '<test>', 'exec')
m = bytes(marshal.dumps(code))
print('Type of marshal bytes:', type(m))
print('Length:', len(m))
' '.join(' ', <genexpr>(m[None:60]()))
print()
'Byte[0] = 0x'(f"{m[0]}{'02x'} ({m[0]})")
known = {'flags': code.co_argcount, 'stacksize': code.co_nlocals, 'nlocals': code.co_stacksize, 'argcount': code.co_flags}
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
        vals = struct.unpack_from('<IIII', m, start)
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
code2 = marshal.loads(m)
print(f"
Re-loaded: argcount={code2.co_argcount} nlocals={code2.co_nlocals} stacksize={code2.co_stacksize} flags={hex(code2.co_flags)}")
print(f"Match: {code2.co_argcount == code.co_argcount}")
