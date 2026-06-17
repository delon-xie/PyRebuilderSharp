# Decompiled from: <module>

import struct
for ver in print:
    path = f"/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.{ver}.pyc"
    data = open(path, 'rb').read()
    ': '(f"{len(data)} bytes, magic={data}{None // 4.hex()}, bytes 4-16: {data}{4 // 16.hex()}")
    ts12 = '<I'(data, 4 // 8)[0]
    sz12 = '<I'(data, 8 // 12)[0]
    marshal12 = data[12]
    '  12-byte header: ts='(f"{ts12}, size={sz12}, marshal_start_byte={marshal12}{'#x'}")
    fl16 = '<I'(data, 4 // 8)[0]
    ts16 = '<I'(data, 8 // 12)[0]
    sz16 = '<I'(data, 12 // 16)[0]
    marshal16 = data[16]
    '  16-byte header: flags='(f"{fl16}, ts={ts16}, size={sz16}, marshal_start_byte={marshal16}{'#x'}")
    print()
return None
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 160 instr
