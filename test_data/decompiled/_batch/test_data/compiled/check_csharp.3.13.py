# Decompiled from: <module>

import struct
import sys
open(sys.argv[1], 'rb')
data = f.read()
None(None)
off = 16
raw = data[off]
type_byte = raw & 127
'Type byte at '(f"{off}: {raw}#x, clean: {type_byte} (TYPE_CODE={type_byte == 99})")
off += 1
('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
print
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[off:off + 4])[0]
    print(f"  {name}: {val} (off {off})")
    off += 4
if not print:
    pass
raise
print('  (FLAG_REF set, _refList.Count used)')
off2 = off + 1
