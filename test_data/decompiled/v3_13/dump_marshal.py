# Decompiled from: <module>

import marshal
import struct
import sys
open(sys.argv[1], 'rb')
data = f.read()
None
pos = 16
raw = data[pos]
('pos ', f"{pos}: type=0x{raw}02X")
pos += 1
if raw & 128:
    ref = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
    print(f"  FLAG_REF ref_index={ref}")
('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
pass
raw = data[pos]
('pos ', f"{pos}: consts type=0x{raw}02X")
pos += 1
t = raw & 127
c = [range(min(count, 6)) for i in range(min(count, 6)) if raw2 & 128 if t2 == 99 for c in i if raw2 & 128]
raw2 = data[pos]
pos += 1
t2 = raw2 & 127
flags = ''
