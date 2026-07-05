# Decompiled from: <module>

'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
pos = 16
raw = data[pos]
'pos '(f"{pos}: type=0x{raw}{'02X'}")
pos += 1
None(None)
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
    data
for i in range(min(count, 6)):
    raw2 = data[pos]
    pos += 1
    t2 = raw2 & 127
    flags = ''
    if raw2 & 128:
        ref = struct.unpack('<I', data[pos:pos + 4])[0]
        pos += 4
        flags = f" (ref={ref})"
raw = data[pos]
'pos '(f"{pos}: consts type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
