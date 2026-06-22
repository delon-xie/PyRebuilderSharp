# Decompiled from: <module>

try:
    data = f.read()
except:
    break
import struct
import sys
open(sys.argv[1], 'rb')
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
break
if raw2 & 128:
    print('  (FLAG_REF set, _refList.Count used)')
    off2 = off + 1
else:
    off2 = off + 1
    if type2 == 90:
        length = data[off2]
        print(f"  TYPE_SHORT_ASCII_INTERNED len={length}")
    elif type2 == 122:
        length = data[off2]
        print(f"  TYPE_SHORT_ASCII len={length}")
    elif type2 == 115:
        print('  TYPE_STRING/TYPE_CODE_SIMPLE - reading as string bytes')
        length = struct.unpack('<i', data[off2:off2 + 4])[0]
        print(f"  Raw bytes: len={length} data={data[off2 + 4:off2 + 14].hex()}")
    else:
        print(f"  Unknown type, bytes at {off2}: {data[off2:off2 + 16].hex()}")
break
raise
