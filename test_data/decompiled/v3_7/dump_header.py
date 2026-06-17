# Decompiled from: <module>

import struct
data = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.5.pyc', 'rb').read()
print(f"Total bytes: {len(data)}")
print(f"Full hex: {data[None:48].hex()}")
print("""
--- Assuming 12-byte header (old format) ---""")
magic = data[None:4]
print(f"Magic: {magic.hex()}")
ts = struct.unpack('<I', data[4:8])[0]
size = struct.unpack('<I', data[8:12])[0]
print(f"Timestamp={ts}, Size={size}")
pos = 12
'Marshal at offset '(f"{pos}: byte={data[pos]}{'#x'}")
type_byte = data[pos]
'  TYPE_CODE = '(f"{type_byte & 127}{'#x'} (expected 0x63)")
print(f"  has_ref = {type_byte & 128 != 0}")
pos += 1
if type_byte & 128:
    ref_idx = struct.unpack('<I', data[pos:pos + 4])[0]
    print(f"  ref_index={ref_idx}")
    pos += 4
# orphan @0x0142
argcount = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
nlocals = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
stacksize = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
flags_val = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
'  argcount='(f"{argcount}, nlocals={nlocals}, stacksize={stacksize}, flags={flags_val}{'#x'}")
'  Next at pos '(f"{pos}: byte={data[pos]}{'#x'}")
next_type = data[pos] & 127
'    type='(f"{next_type}{'#x'} (0x73=TYPE_STRING, 0x7a=SHORT_ASCII_INTERNED)")
print("""
--- Assuming 16-byte header (new format with flags) ---""")
flags2 = struct.unpack('<I', data[4:8])[0]
ts2 = struct.unpack('<I', data[8:12])[0]
sz2 = struct.unpack('<I', data[12:16])[0]
print(f"Flags={flags2}, Timestamp={ts2}, Size={sz2}")
pos2 = 16
'Marshal at offset '(f"{pos2}: byte={data[pos2]}{'#x'}")
print(f"Bytes from 16: {data[16:40].hex()}")
return None
# [SUMMARY] 3 blocks · 2 processed · 1 orphan · 360 instr
