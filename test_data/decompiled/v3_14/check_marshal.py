# Decompiled from: <module>

# orphan @0x0104
ref_idx = struct.unpack('<I', data[pos + 1:pos + 5])[0]
fields_start = pos + 5
print(f"  ref_index={ref_idx} at {pos + 1}-{pos + 4}")
print(f"  fields_at={fields_start}")
argcount = struct.unpack('<I', data[fields_start:fields_start + 4])[0]
print(f"  argcount={argcount}")
posOnly = struct.unpack('<I', data[fields_start + 4:fields_start + 8])[0]
# orphan @0x00F2
# orphan @0x00E4
# orphan @0x00E2
# orphan @0x00BC
# orphan @0x0070
hdr = 12
hdr = 16
pos = hdr
type_byte = data[pos]
actual_type = type_byte & 127
has_ref = type_byte & 128 != 0
# orphan @0x005C
hdr = 8
# orphan @0x0014
path = f"/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.{ver}.pyc"
data = open(path, 'rb').read()
# orphan @0x0000
import struct
# orphan @0x0282
print(f"  posOnlyArgCount={posOnly}")
nlocals = struct.unpack('<I', data[fields_start + 12:fields_start + 16])[0]
nlocals = struct.unpack('<I', data[fields_start + 4:fields_start + 8])[0]
print(f"  nlocals={nlocals}")
print('  No FLAG_REF')
fields_start = pos + 1
print(f"  fields_at={fields_start}")
argcount = struct.unpack('<I', data[fields_start:fields_start + 4])[0]
print(f"  argcount={argcount}")
print()
return None
# [SUMMARY] 16 blocks · 7 processed · 15 orphan · 273 instr
