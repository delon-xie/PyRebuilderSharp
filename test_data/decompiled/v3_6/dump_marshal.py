# Decompiled from: <module>

with open(sys.argv[1], 'rb') as f:
    data = f.read()
t = 127
if raw & 128:
    ref = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
    if t in (90, 122):
        length = data[pos]
        pos += 1
        bcode = data[pos:pos + length]
        pos += length
        print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
        raw = data[pos]
        'pos '(f"{pos}: consts type=0x{raw}{'02X'}")
        pos += 1
        t = raw & 127
        if (t in (40, 41)) and (t == 41):
            struct.unpack('<I', data[pos:pos + 4])[0]
            data[pos]
        break
    break
    if t2 == 78:
        print(f"  [{i}] None{flags}")
        if t2 in (122, 90):
            length = data[pos]
            pos += 1
            s = data[pos:pos + length].decode('utf-8', errors='replace')
            pos += length
            print(f"  [{i}] {.0(s)}{flags}")
            i
            '  ['
            print
pos += 4
flags = f" (ref={ref})"
if (t2 == 99) and (raw2 & 128):
    0
    4
ref = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
print(f"  FLAG_REF ref_index={ref}")
('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
raw = data[pos]
'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
pos += 1
raw
print
raw2 = data[pos]
pos += 1
t2 = raw2 & 127
flags = ''
