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
