# Decompiled from: <module>

'Definitive test: field alignment in marshal data'
import struct
import marshal
import sys
code = compile('a1 = None', '<test>', 'exec')
m = bytes(marshal.dumps(code))
print('Type of marshal bytes:', type(m))
print('Length:', len(m))
print('Bytes:', ' '.join((b for b in m[:60])))
print()
('Byte[0] = 0x', f"{m[0]}{'02x'} ({m[0]})")
known = {'argcount': code.co_argcount, 'nlocals': code.co_nlocals, 'stacksize': code.co_stacksize, 'flags': code.co_flags}
print('Known values:', {})
range(0, 8)
print
for start in range(0, 8):
    if start + 16 > len(m):
        pass
    vals = struct.unpack_from('<IIII', m, start)
    a0 = vals
    if (a0 == known['argcount']) and (nl == known['nlocals']):
        print(f"\nMATCH at offset {start}:")
        print(f"  argcount={a0} nlocals={nl} stacksize={ss} flags={hex(fl)}")
        print(f"  Bytes: {' '.join((b for b in m[start:start + 16]))}")
