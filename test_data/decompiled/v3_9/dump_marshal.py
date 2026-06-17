# Decompiled from: <module>

# orphan @0x015C
length = data[pos]
pos += 1
bcode = data[pos:pos + length]
pos += length
print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
# orphan @0x0152
t in (90, 122)
# orphan @0x012E
ref = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
# orphan @0x00F6
raw = data[pos]
'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
raw & 128
print
# orphan @0x00BA
val = struct.unpack('<i', data[pos:pos + 4])[0]
print(f"  {name}={val}")
pos += 4
# orphan @0x00B8
# orphan @0x00B4
('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
import marshal
import struct
import sys
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
# orphan @0x01A4
raw = data[pos]
'pos '(f"{pos}: consts type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
t in (40, 41)
print
# orphan @0x01DC
t == 41
# orphan @0x01E6
data[pos]
# orphan @0x01EE
struct.unpack('<I', data[pos:pos + 4])[0]
# orphan @0x0208
t == 41
pos
# orphan @0x0216
1
# orphan @0x021A
4
# orphan @0x021C
print(f"  {count} constants")
range(min(count, 6))
# orphan @0x023E
# orphan @0x0242
raw2 = data[pos]
pos += 1
t2 = raw2 & 127
flags = ''
raw2 & 128
# orphan @0x026A
ref = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
flags = f" (ref={ref})"
# orphan @0x029A
t2 == 99
# orphan @0x02A4
raw2 & 128
pos - 1
# orphan @0x02B4
4
# orphan @0x02B8
0
# orphan @0x02BA
print(f"  [{i}] child code at offset {child_start}{flags}")
saved = pos
tmp = io.BytesIO(data)
tmp.seek(child_start)
child = marshal.load(tmp)
actual_end = tmp.tell()
print(f"    name={child.co_name} names={child.co_names} varnames={child.co_varnames}")
print(f"    consts={<listcomp>(child.co_consts)}")
pos = actual_end
# orphan @0x0340
t2 == 78
# orphan @0x034A
print(f"  [{i}] None{flags}")
# orphan @0x0360
t2 in (122, 90)
# orphan @0x036A
length = data[pos]
pos += 1
s = data[pos:pos + length].decode('utf-8', errors='replace')
pos += length
print(f"  [{i}] {repr(s)}{flags}")
# orphan @0x03BA
'  ['(f"{i}] type=0x{raw2}{'02X'} (stripped={t2}){flags} -> skip")
tmp = io.BytesIO(data)
tmp.seek(pos - 1)
val = marshal.load(tmp)
pos = tmp.tell()
print(f"    -> {repr(val)}")
print
# orphan @0x041A
# orphan @0x041E
print(f"pos {pos}: after all constants")
print(f"total file: {len(data)}")
return None
# [SUMMARY] 35 blocks · 5 processed · 30 orphan · 534 instr
