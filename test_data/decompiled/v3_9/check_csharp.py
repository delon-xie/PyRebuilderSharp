# Decompiled from: <module>

import struct
import sys
with open(sys.argv[1], 'rb') as f:
    data = f.read()
    for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
        val = struct.unpack('<i', data[off:off + 4])[0]
        print(f"  {name}: {val} (off {off})")
        off = off + 4
# orphan @0x00D6
'Next marshal at off='(f"{off}, byte={data[off]}{'#x'}")
raw2 = data[off]
type2 = raw2 & 127
'  type_byte='(f"{raw2}{'#x'}, clean={type2}")
# orphan @0x0120
print('  (FLAG_REF set, _refList.Count used)')
off2 = off + 1
# orphan @0x0132
off2 = off + 1
# orphan @0x013A
# orphan @0x0144
length = data[off2]
print(f"  TYPE_SHORT_ASCII_INTERNED len={length}")
# orphan @0x015C
# orphan @0x0166
length = data[off2]
print(f"  TYPE_SHORT_ASCII len={length}")
# orphan @0x017E
# orphan @0x0188
print('  TYPE_STRING/TYPE_CODE_SIMPLE - reading as string bytes')
length = struct.unpack('<i', data[off2:off2 + 4])[0]
print(f"  Raw bytes: len={length} data={data[off2 + 4:off2 + 14].hex()}")
# orphan @0x01D6
print(f"  Unknown type, bytes at {off2}: {data[off2:off2 + 16].hex()}")
# [SUMMARY] 17 blocks · 6 processed · 11 orphan · 251 instr
