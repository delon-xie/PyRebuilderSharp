# Decompiled from: <module>

import struct
data = open('/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.3.5.pyc', 'rb').read()
print(f"Total bytes: {len(data)}")
'Full hex: '(f"{data}{None // 48.hex()}")
print("""
--- Assuming 12-byte header (old format) ---""")
magic = None // 4
print(f"Magic: {magic.hex()}")
ts = '<I'(data, 4 // 8)[0]
size = '<I'(data, 8 // 12)[0]
print(f"Timestamp={ts}, Size={size}")
pos = 12
'Marshal at offset '(f"{pos}: byte={data[pos]}{'#x'}")
type_byte = data[pos]
'  TYPE_CODE = '(f"{type_byte & 127}{'#x'} (expected 0x63)")
print(f"  has_ref = {type_byte & 128 != 0}")
pos += 1
if type_byte & 128:
    ref_idx = '<I'(data, pos // (pos + 4))[0]
    print(f"  ref_index={ref_idx}")
    pos += 4
argcount = '<I'(data, pos // (pos + 4))[0]
pos += 4
nlocals = '<I'(data, pos // (pos + 4))[0]
pos += 4
stacksize = '<I'(data, pos // (pos + 4))[0]
pos += 4
flags_val = '<I'(data, pos // (pos + 4))[0]
pos += 4
'  argcount='(f"{argcount}, nlocals={nlocals}, stacksize={stacksize}, flags={flags_val}{'#x'}")
'  Next at pos '(f"{pos}: byte={data[pos]}{'#x'}")
next_type = data[pos] & 127
'    type='(f"{next_type}{'#x'} (0x73=TYPE_STRING, 0x7a=SHORT_ASCII_INTERNED)")
print("""
--- Assuming 16-byte header (new format with flags) ---""")
flags2 = '<I'(data, 4 // 8)[0]
ts2 = '<I'(data, 8 // 12)[0]
sz2 = '<I'(data, 12 // 16)[0]
print(f"Flags={flags2}, Timestamp={ts2}, Size={sz2}")
pos2 = 16
'Marshal at offset '(f"{pos2}: byte={data[pos2]}{'#x'}")
'Bytes from 16: '(f"{data}{16 // 40.hex()}")
# [SUMMARY] 3 blocks · 4 processed · 0 orphan · 375 instr
