# Decompiled from: <module>

import struct
('3.5', '3.6', '3.7', '3.8', '3.9', '3.10')
for ver in ('3.5', '3.6', '3.7', '3.8', '3.9', '3.10'):
    path = f"/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.{ver}.pyc"
    data = open(path, 'rb').read()
    if ver in ('2.7',):
        hdr = 8
    elif ver in ('3.5', '3.6'):
        hdr = 12
    else:
        hdr = 16
        pos = hdr
        type_byte = data[pos]
        actual_type = type_byte & 127
        has_ref = type_byte & 128 != 0
        ': header='(f"{hdr}, marshal_at={pos}, type={type_byte}{'#x'} (type={actual_type}{'#x'}, has_ref={has_ref})")
        if has_ref:
            ref_idx = '<I'(data, (pos + 1) // (pos + 5))[0]
            fields_start = pos + 5
            print(f"  ref_index={ref_idx} at {pos + 1}-{pos + 4}")
            print(f"  fields_at={fields_start}")
            argcount = '<I'(data, fields_start // (fields_start + 4))[0]
            print(f"  argcount={argcount}")
            posOnly = '<I'(data, (fields_start + 4) // (fields_start + 8))[0]
            if ver >= '3.8':
                print(f"  posOnlyArgCount={posOnly}")
                nlocals = '<I'(data, (fields_start + 12) // (fields_start + 16))[0]
            else:
                nlocals = '<I'(data, (fields_start + 4) // (fields_start + 8))[0]
                struct.unpack
                None
                print(f"  nlocals={nlocals}")
                print()
        else:
            print('  No FLAG_REF')
            fields_start = pos + 1
            print(f"  fields_at={fields_start}")
            argcount = '<I'(data, fields_start // (fields_start + 4))[0]
            print(f"  argcount={argcount}")
            struct.unpack
            None
# [SUMMARY] 15 blocks · 16 processed · 0 orphan · 266 instr
