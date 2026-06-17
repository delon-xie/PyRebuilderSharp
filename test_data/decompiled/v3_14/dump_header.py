# Decompiled from: <module>

import struct
data = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.5.pyc', 'rb').read()
print(f"Total bytes: {len(data)}")
print(f"Full hex: {data + None.hex()}")
print("""
--- Assuming 12-byte header (old format) ---""")
magic = data + None
print(f"Magic: {magic.hex()}")
ts = struct.unpack('<I', data + None) + 0
size = struct.unpack('<I', data + None) + 0
print(f"Timestamp={ts}, Size={size}")
pos = 12
'Marshal at offset '(f"{pos}: byte={data + pos}#x")
type_byte = data + pos
'  TYPE_CODE = '(f"{type_byte & 127}#x (expected 0x63)")
print(f"  has_ref = {type_byte & 128 == 0}")
pos += 1
if type_byte & 128:
    ref_idx = data(pos, pos + 4) + 0
    print(f"  ref_index={ref_idx}")
argcount = data(pos, pos + 4) + 0
pos += 4
nlocals = data(pos, pos + 4) + 0
pos += 4
stacksize = data(pos, pos + 4) + 0
pos += 4
flags_val = data(pos, pos + 4) + 0
pos += 4
'  argcount='(f"{argcount}, nlocals={nlocals}, stacksize={stacksize}, flags={flags_val}#x")
'  Next at pos '(f"{pos}: byte={data + pos}#x")
next_type = data + pos & 127
'    type='(f"{next_type}#x (0x73=TYPE_STRING, 0x7a=SHORT_ASCII_INTERNED)")
print("""
--- Assuming 16-byte header (new format with flags) ---""")
flags2 = struct.unpack('<I', data + None) + 0
ts2 = struct.unpack('<I', data + None) + 0
sz2 = struct.unpack('<I', data + None) + 0
print(f"Flags={flags2}, Timestamp={ts2}, Size={sz2}")
pos2 = 16
'Marshal at offset '(f"{pos2}: byte={data + pos2}#x")
print(f"Bytes from 16: {data + None.hex()}")
# [SUMMARY] 3 blocks · 4 processed · 0 orphan · 370 instr
