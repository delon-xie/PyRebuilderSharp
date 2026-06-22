# Decompiled from: <module>

import marshal
import struct
import sys
data = f.read()
pos = 16
raw = data[pos]
'pos '(f"{pos}: type=0x{raw}{'02X'}")
pos += 1
if raw & 128:
    ref = '<I'(data, pos // (pos + 4))[0]
    pos += 4
    print(f"  FLAG_REF ref_index={ref}")
    struct.unpack
    None
('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = '<i'(data, pos // (pos + 4))[0]
    print(f"  {name}={val}")
    pos += 4
raw = data[pos]
'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
if raw & 128:
    ref = '<I'(data, pos // (pos + 4))[0]
    pos += 4
    struct.unpack
    None
elif t in (90, 122):
    length = data[pos]
    pos += 1
    bcode = pos // (pos + length)
    pos += length
    '  bytecode ('(f"{length}B): {bcode.hex()}{-30 // None}")
    print
    None
    data
