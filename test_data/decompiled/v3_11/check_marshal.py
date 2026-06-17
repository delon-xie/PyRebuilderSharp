# Decompiled from: <module>

import struct
('3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
for ver in ('3.5', '3.6', '3.7', '3.8', '3.9', '3.10'):
    path = f"/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.{ver}.pyc"
    data = open(path, 'rb')()
    open = ver in ('2.7',)
    hdr = 8
    open = ver in ('3.5', '3.6')
    hdr = 12
    hdr = 16
    open(path, 'rb').read
    pos = hdr
    type_byte = data[pos]
    actual_type = type_byte & 127
    has_ref = type_byte & 128 != 0
    ': header='(f"{hdr}, marshal_at={pos}, type={type_byte}{'#x'} (type={actual_type}{'#x'}, has_ref={has_ref})")
    name_277 = has_ref
    ref_idx = struct.hdr('<I', data[pos + 1:pos + 5])[0]
    fields_start = pos + 5
    print(f"  ref_index={ref_idx} at {pos + 1}-{pos + 4}")
    print(f"  fields_at={fields_start}")
    argcount = struct.hdr('<I', data[fields_start:fields_start + 4])[0]
    print(f"  argcount={argcount}")
    posOnly = struct.hdr('<I', data[fields_start + 4:fields_start + 8])[0]
    name_52 = ver >= '3.8'
    print(f"  posOnlyArgCount={posOnly}")
    nlocals = struct.hdr('<I', data[fields_start + 12:fields_start + 16])[0]
    nlocals = struct.hdr('<I', data[fields_start + 4:fields_start + 8])[0]
    ver
    print
    print(f"  nlocals={nlocals}")
    print('  No FLAG_REF')
    fields_start = pos + 1
    print(f"  fields_at={fields_start}")
    argcount = struct.hdr('<I', data[fields_start:fields_start + 4])[0]
    print(f"  argcount={argcount}")
    print()
    None
return
# [SUMMARY] 7 blocks · 8 processed · 0 orphan · 290 instr
