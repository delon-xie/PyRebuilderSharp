# Decompiled from: <module>

raw = data[pos]
'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
import marshal
import struct
import sys
f = open(sys.argv[1], 'rb')
data = f.read()
pos = 16
raw = data[pos]
'pos '(f"{pos}: type=0x{raw}{'02X'}")
pos += 1
with open(sys.argv[1], 'rb') as f:
    data = f.read()
('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
raw = data[pos]
'pos '(f"{pos}: consts type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
for i in range(min(count, 6)):
    raw2 = data[pos]
    pos += 1
    t2 = raw2 & 127
    flags = ''
    if raw2 & 128:
        ref = struct.unpack('<I', data[pos:pos + 4])[0]
        pos += 4
        flags = f" (ref={ref})"
    if (t2 == 99) and (raw2 & 128):
        pass
    if t2 == 78:
        print(f"  [{i}] None{flags}")
    if t2 in (122, 90):
        length = data[pos]
        pos += 1
        s = data[pos:pos + length].decode('utf-8', errors='replace')
        pos += length
        print(f"  [{i}] {.0(s)}{flags}")
    0
    '  ['(f"{i}] type=0x{raw2}{'02X'} (stripped={t2}){flags} -> skip")
    tmp = io.BytesIO(data)
    tmp.seek(pos - 1)
    val = marshal.load(tmp)
    pos = tmp.tell()
    print(f"    -> {.0(val)}")
    print
    print(f"  [{i}] child code at offset {child_start}{flags}")
    saved = pos
    tmp = io.BytesIO(data)
    tmp.seek(child_start)
    child = marshal.load(tmp)
    actual_end = tmp.tell()
    print(f"    name={child.co_name} names={child.co_names} varnames={child.co_varnames}")
    print(f"    consts={[c for c in iterable]}")
    pos = actual_end
raw2 = data[pos]
pos += 1
t2 = raw2 & 127
flags = ''
print(f"  [{i}] None{flags}")
length = data[pos]
pos += 1
s = data[pos:pos + length].decode('utf-8', errors='replace')
pos += length
print(f"  [{i}] {.0(s)}{flags}")
