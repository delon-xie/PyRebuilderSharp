# Decompiled from: <module>

import struct
import sys
with open(sys.argv[1], 'rb') as f:
    data = f.read()
    raise
    for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
        val = struct.unpack('<i', data[off:off + 4])[0]
        print(f"  {name}: {val} (off {off})")
        off = off + 4
# orphan @0x00D6
'Next marshal at off='(f"{off}, byte={data[off]}{'#x'}")
raw2 = data[off]
type2 = raw2 & 127
'  type_byte='(f"{raw2}{'#x'}, clean={type2}")
raw2 & 128
print
print
# orphan @0x011E
print('  (FLAG_REF set, _refList.Count used)')
off2 = off + 1
# orphan @0x0130
off2 = off + 1
# orphan @0x0138
type2 == 90
# orphan @0x0140
length = data[off2]
print(f"  TYPE_SHORT_ASCII_INTERNED len={length}")
return None
# orphan @0x015A
type2 == 122
# orphan @0x0162
length = data[off2]
print(f"  TYPE_SHORT_ASCII len={length}")
return None
# orphan @0x017C
type2 == 115
# orphan @0x0184
print('  TYPE_STRING/TYPE_CODE_SIMPLE - reading as string bytes')
length = struct.unpack('<i', data[off2:off2 + 4])[0]
print(f"  Raw bytes: len={length} data={data[off2 + 4:off2 + 14].hex()}")
return None
# orphan @0x01D4
print(f"  Unknown type, bytes at {off2}: {data[off2:off2 + 16].hex()}")
return None
# [SUMMARY] 16 blocks · 6 processed · 10 orphan · 254 instr
