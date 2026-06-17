# Decompiled from: <module>

# orphan @0x014C
length = data[pos]
pos += 1
bcode = data[pos:pos + length]
pos += length
print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
# orphan @0x0142
t in (90, 122)
import marshal
import struct
import sys
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
# orphan @0x0194
raw = data[pos]
'pos '(f"{pos}: consts type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
t in (40, 41)
print
# orphan @0x01CC
t == 41
# orphan @0x01D6
data[pos]
# orphan @0x01DE
struct.unpack('<I', data[pos:pos + 4])[0]
# orphan @0x01F8
t == 41
pos
# orphan @0x0206
1
# orphan @0x020A
4
# orphan @0x020C
print(f"  {count} constants")
range(min(count, 6))
# orphan @0x0232
# orphan @0x0236
raw2 = data[pos]
pos += 1
t2 = raw2 & 127
flags = ''
raw2 & 128
# orphan @0x025E
ref = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
flags = f" (ref={ref})"
# orphan @0x028E
t2 == 99
# orphan @0x0298
raw2 & 128
pos - 1
# orphan @0x02A8
4
# orphan @0x02AC
0
# orphan @0x02AE
print(f"  [{i}] child code at offset {child_start}{flags}")
saved = pos
tmp = io.BytesIO(data)
tmp.seek(child_start)
child = marshal.load(tmp)
actual_end = tmp.tell()
print(f"    name={child.co_name} names={child.co_names} varnames={child.co_varnames}")
print(f"    consts={<lambda>(child.co_consts)}")
pos = actual_end
# orphan @0x0334
t2 == 78
# orphan @0x033E
print(f"  [{i}] None{flags}")
# orphan @0x0354
t2 in (122, 90)
# orphan @0x035E
length = data[pos]
pos += 1
s = data[pos:pos + length].decode('utf-8', errors='replace')
pos += length
print(f"  [{i}] {.0(s)}{flags}")
# orphan @0x03AE
'  ['(f"{i}] type=0x{raw2}{'02X'} (stripped={t2}){flags} -> skip")
tmp = io.BytesIO(data)
tmp.seek(pos - 1)
val = marshal.load(tmp)
pos = tmp.tell()
print(f"    -> {.0(val)}")
print
# orphan @0x040E
# orphan @0x0412
# orphan @0x0414
print(f"pos {pos}: after all constants")
print(f"total file: {len(data)}")
return None
# [SUMMARY] 33 blocks · 7 processed · 26 orphan · 528 instr
