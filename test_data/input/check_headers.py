import struct
for ver in ['3.5', '3.6', '3.7', '3.8']:
    path = f'/Users/admin/codes/Tools/PyRebuilderSharp/tests/PyRebuilderSharp.Tests/TestData/compiled/test_expr_basic.{ver}.pyc'
    data = open(path, 'rb').read()
    print(f'{ver}: {len(data)} bytes, magic={data[:4].hex()}, bytes 4-16: {data[4:16].hex()}')
    # Try 12-byte header
    ts12 = struct.unpack('<I', data[4:8])[0]
    sz12 = struct.unpack('<I', data[8:12])[0]
    marshal12 = data[12]
    print(f'  12-byte header: ts={ts12}, size={sz12}, marshal_start_byte={marshal12:#x}')
    # Try 16-byte header
    fl16 = struct.unpack('<I', data[4:8])[0]
    ts16 = struct.unpack('<I', data[8:12])[0]
    sz16 = struct.unpack('<I', data[12:16])[0]
    marshal16 = data[16]
    print(f'  16-byte header: flags={fl16}, ts={ts16}, size={sz16}, marshal_start_byte={marshal16:#x}')
    print()
