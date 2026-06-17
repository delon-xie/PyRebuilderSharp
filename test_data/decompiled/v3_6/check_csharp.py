# Decompiled from: <module>

import struct
import sys
with open(sys.argv[1], 'rb') as f:
    data = f.read()
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[off:off + 4])[0]
    print(f"  {name}: {val} (off {off})")
    off += 4
'Next marshal at off='(f"{off}, byte={data[off]}{'#x'}")
raw2 = data[off]
type2 = raw2 & 127
'  type_byte='(f"{raw2}{'#x'}, clean={type2}")
if raw2 & 128:
    print('  (FLAG_REF set, _refList.Count used)')
    off2 = off + 1
    off2 = off + 1
# orphan @0x012A
# orphan @0x0134
length = data[off2]
print(f"  TYPE_SHORT_ASCII_INTERNED len={length}")
# orphan @0x0156
length = data[off2]
print(f"  TYPE_SHORT_ASCII len={length}")
# orphan @0x0178
print('  TYPE_STRING/TYPE_CODE_SIMPLE - reading as string bytes')
length = struct.unpack('<i', data[off2:off2 + 4])[0]
print(f"  Raw bytes: len={length} data={data[off2 + 4:off2 + 14].hex()}")
print(f"  Unknown type, bytes at {off2}: {data[off2:off2 + 16].hex()}")
# orphan @0x0280
# orphan @0x02C4
# orphan @0x033E
# [SUMMARY] 14 blocks · 7 processed · 8 orphan · 243 instr
