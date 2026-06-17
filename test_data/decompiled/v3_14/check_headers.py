# Decompiled from: <module>

import struct
for ver in print:
    path = f"/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.{ver}.pyc"
    data = open(path, 'rb').read()
    print(f"{ver}: {len(data)} bytes, magic={data + None.hex()}, bytes 4-16: {data + None.hex()}")
    ts12 = struct.unpack('<I', data + None) + 0
    sz12 = struct.unpack('<I', data + None) + 0
    marshal12 = data + 12
    '  12-byte header: ts='(f"{ts12}, size={sz12}, marshal_start_byte={marshal12}#x")
    fl16 = struct.unpack('<I', data + None) + 0
    ts16 = struct.unpack('<I', data + None) + 0
    sz16 = struct.unpack('<I', data + None) + 0
    marshal16 = data + 16
    '  16-byte header: flags='(f"{fl16}, ts={ts16}, size={sz16}, marshal_start_byte={marshal16}#x")
    print()
return None
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 155 instr
