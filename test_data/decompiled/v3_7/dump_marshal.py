# Decompiled from: <module>

length = data[pos]
pos += 1
bcode = data[pos:pos + length]
pos += length
print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
with open(sys.argv[1], 'rb') as f:
    data = f.read()
('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
raw = data[pos]
'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
if raw & 128:
    ref = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
ref = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
print(f"  FLAG_REF ref_index={ref}")
raw = data[pos]
'pos '(f"{pos}: consts type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
# orphan @0x01DE
struct.unpack('<I', data[pos:pos + 4])[0]
# orphan @0x020A
4
raw2 = data[pos]
pos += 1
t2 = raw2 & 127
flags = ''
ref = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
flags = f" (ref={ref})"
# orphan @0x02AC
0
print(f"  [{i}] None{flags}")
length = data[pos]
pos += 1
s = data[pos:pos + length].decode('utf-8', errors='replace')
pos += length
print(f"  [{i}] {.0(s)}{flags}")
'  ['(f"{i}] type=0x{raw2}{'02X'} (stripped={t2}){flags} -> skip")
tmp = io.BytesIO(data)
tmp.seek(pos - 1)
val = marshal.load(tmp)
pos = tmp.tell()
print(f"    -> {.0(val)}")
print(f"pos {pos}: after all constants")
print(f"total file: {len(data)}")
# [SUMMARY] 33 blocks · 30 processed · 26 orphan · 528 instr
