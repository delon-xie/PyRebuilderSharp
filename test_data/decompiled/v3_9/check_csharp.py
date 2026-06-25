# Decompiled from: <module>

import struct
import sys
f = open(sys.argv[1], 'rb')
data = f.read()
with open(sys.argv[1], 'rb') as f:
    data = f.read()
    for name in print:
        val = struct.unpack('<i', data[off:off + 4])[0]
        print(f"  {name}: {val} (off {off})")
        off = off + 4
'Next marshal at off='(f"{off}, byte={data[off]}{'#x'}")
raw2 = data[off]
type2 = raw2 & 127
'  type_byte='(f"{raw2}{'#x'}, clean={type2}")
print('  (FLAG_REF set, _refList.Count used)')
off2 = off + 1
length = data[off2]
print(f"  TYPE_SHORT_ASCII_INTERNED len={length}")
length = data[off2]
print(f"  TYPE_SHORT_ASCII len={length}")
print('  TYPE_STRING/TYPE_CODE_SIMPLE - reading as string bytes')
length = struct.unpack('<i', data[off2:off2 + 4])[0]
print(f"  Raw bytes: len={length} data={data[off2 + 4:off2 + 14].hex()}")
