# Simulate C# marshal reading for v3.11 .pyc
import struct, sys

with open(sys.argv[1], 'rb') as f:
    data = f.read()

off = 16  # after header

# ReadMarshalObject: read raw type byte
raw = data[off]
type_byte = raw & 0x7f
print(f'Type byte at {off}: {raw:#x}, clean: {type_byte} (TYPE_CODE={type_byte==99})')
off += 1

# FLAG_REF: _refList.Count as index, NO stream skip

# ReadMarshalValue -> ReadMarshalCodeObject(isSimple=False)
# Fields (3.8+ format): 6 int32s
for name in ['argcount','posonly','kwonly','nlocals','stacksize','flags']:
    val = struct.unpack('<i', data[off:off+4])[0]
    print(f'  {name}: {val} (off {off})')
    off += 4

print(f'Next marshal at off={off}, byte={data[off]:#x}')

# This should be the bytecode (a marshal bytes object)
raw2 = data[off]
type2 = raw2 & 0x7f
print(f'  type_byte={raw2:#x}, clean={type2}')

if raw2 & 0x80:
    print(f'  (FLAG_REF set, _refList.Count used)')
    off2 = off + 1
else:
    off2 = off + 1

if type2 == 0x5A:  # TYPE_SHORT_ASCII_INTERNED
    length = data[off2]
    print(f'  TYPE_SHORT_ASCII_INTERNED len={length}')
elif type2 == 0x7A:  # TYPE_SHORT_ASCII
    length = data[off2]
    print(f'  TYPE_SHORT_ASCII len={length}')
elif type2 == 115:  # TYPE_STRING or TYPE_CODE_SIMPLE
    print(f'  TYPE_STRING/TYPE_CODE_SIMPLE - reading as string bytes')
    length = struct.unpack('<i', data[off2:off2+4])[0]
    print(f'  Raw bytes: len={length} data={data[off2+4:off2+14].hex()}')
else:
    print(f'  Unknown type, bytes at {off2}: {data[off2:off2+16].hex()}')
