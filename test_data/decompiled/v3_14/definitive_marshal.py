# Decompiled from: <module>

import struct
import marshal
import sys
code = compile('a1 = None', '<test>', 'exec')
m = bytes(marshal.dumps(code))
print('Type of marshal bytes:', type(m))
print('Length:', len(m))
('02x' for b in iterable)
' '.join
'Bytes:'
None
print
print()
0
m
'Byte[0] = 0x'
None
print
vals = struct.unpack_from('<IIII', m, start)
a0 = *vals
nl = *vals
ss = *vals
fl = *vals
for start in range(0, 8):
    16
    start
    code2 = marshal.loads(m)
    print(f"\nRe-loaded: argcount={code2.co_argcount} nlocals={code2.co_nlocals} stacksize={code2.co_stacksize} flags={hex(code2.co_flags)}")
    print(f"Match: {code2.co_argcount == code.co_argcount}")
    return None
