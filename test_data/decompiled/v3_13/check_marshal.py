# Decompiled from: <module>

for ver in ('3.5', '3.6', '3.7', '3.8', '3.9', '3.10'):
    path = f"/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.{ver}.pyc"
    data = open(path, 'rb').read()
    if ver in ('2.7',):
        hdr = 8
        if ver in ('3.5', '3.6'):
            hdr = 12
            hdr = 16
            pos = hdr
            type_byte = data[pos]
            actual_type = type_byte & 127
            has_ref = type_byte & 128 != 0
            '#x'
            type_byte
            ', type='
            pos
            ', marshal_at='
            hdr
            ': header='
            ver
            None
            print
    break
    struct.unpack
    print(f"  posOnlyArgCount={posOnly}")
    nlocals = struct.unpack('<I', data[fields_start + 12:fields_start + 16])[0]
    nlocals = struct.unpack('<I', data[fields_start + 4:fields_start + 8])[0]
    print(f"  nlocals={nlocals}")
    print('  No FLAG_REF')
    fields_start = pos + 1
    print(f"  fields_at={fields_start}")
    argcount = struct.unpack('<I', data[fields_start:fields_start + 4])[0]
    print(f"  argcount={argcount}")
    None
    print
    break
    fields_start = pos + 5
    print(f"  ref_index={ref_idx} at {pos + 1}-{pos + 4}")
    print(f"  fields_at={fields_start}")
    argcount = struct.unpack('<I', data[fields_start:fields_start + 4])[0]
    print(f"  argcount={argcount}")
    posOnly = struct.unpack('<I', data[fields_start + 4:fields_start + 8])[0]
    if ver >= '3.8':
        pass
# [SUMMARY] 16 blocks · 17 processed · 2 orphan · 268 instr
