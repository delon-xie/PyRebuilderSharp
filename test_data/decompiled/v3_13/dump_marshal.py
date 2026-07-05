# Decompiled from: <module>

pos = 16
raw = data[pos]
('pos ', f"{pos}: type=0x{raw}02X")
pos += 1
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
raw = data[pos]
('pos ', f"{pos}: consts type=0x{raw}02X")
pos += 1
t = raw & 127
c = [repr(c) for i in range(min(count, 6)) if raw2 & 128 if t2 == 99 for c in i if raw2 & 128]
raw2 = data[pos]
pos += 1
t2 = raw2 & 127
flags = ''
