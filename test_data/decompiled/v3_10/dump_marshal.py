# Decompiled from: <module>

with open(sys.argv[1], 'rb') as f:
    data = f.read()
    pos = 16
    raw = data[pos]
    'pos '(f"{pos}: type=0x{raw}{'02X'}")
    pos = pos + 1
    if raw & 128:
        ref = struct.unpack('<I', data[pos:pos + 4])[0]
        pos = pos + 4
        print(f"  FLAG_REF ref_index={ref}")
    ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
    for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
        val = struct.unpack('<i', data[pos:pos + 4])[0]
        print(f"  {name}={val}")
        pos = pos + 4
    raw = data[pos]
    'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
    pos = pos + 1
    t = raw & 127
    if raw & 128:
        ref = struct.unpack('<I', data[pos:pos + 4])[0]
        pos = pos + 4
    elif t in (90, 122):
        length = data[pos]
        pos = pos + 1
        bcode = data[pos:pos + length]
        pos = pos + length
        print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
