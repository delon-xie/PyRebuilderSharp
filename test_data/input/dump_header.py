import struct

data = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.5.pyc', 'rb').read()
print(f'Total bytes: {len(data)}')
print(f'Full hex: {data[:48].hex()}')

# Try header at 12 bytes
print(f'\n--- Assuming 12-byte header (old format) ---')
magic = data[:4]
print(f'Magic: {magic.hex()}')
ts = struct.unpack('<I', data[4:8])[0]
size = struct.unpack('<I', data[8:12])[0]
print(f'Timestamp={ts}, Size={size}')
pos = 12
print(f'Marshal at offset {pos}: byte={data[pos]:#x}')
type_byte = data[pos]
print(f'  TYPE_CODE = {type_byte & 0x7f:#x} (expected 0x63)')
print(f'  has_ref = {(type_byte & 0x80) != 0}')
pos += 1
if type_byte & 0x80:
    ref_idx = struct.unpack('<I', data[pos:pos+4])[0]
    print(f'  ref_index={ref_idx}')
    pos += 4

argcount = struct.unpack('<I', data[pos:pos+4])[0]; pos += 4
nlocals = struct.unpack('<I', data[pos:pos+4])[0]; pos += 4
stacksize = struct.unpack('<I', data[pos:pos+4])[0]; pos += 4
flags_val = struct.unpack('<I', data[pos:pos+4])[0]; pos += 4
print(f'  argcount={argcount}, nlocals={nlocals}, stacksize={stacksize}, flags={flags_val:#x}')

print(f'  Next at pos {pos}: byte={data[pos]:#x}')
next_type = data[pos] & 0x7f
print(f'    type={next_type:#x} (0x73=TYPE_STRING, 0x7a=SHORT_ASCII_INTERNED)')

print(f'\n--- Assuming 16-byte header (new format with flags) ---')
flags2 = struct.unpack('<I', data[4:8])[0]
ts2 = struct.unpack('<I', data[8:12])[0]
sz2 = struct.unpack('<I', data[12:16])[0]
print(f'Flags={flags2}, Timestamp={ts2}, Size={sz2}')
pos2 = 16
print(f'Marshal at offset {pos2}: byte={data[pos2]:#x}')
# dump 40 bytes from offset 16
print(f'Bytes from 16: {data[16:40].hex()}')
