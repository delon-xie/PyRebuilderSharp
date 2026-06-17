# Decompiled from: <module>

# orphan @0x0148
length = data[pos]
pos += 1
bcode = data[pos:pos + length]
pos += length
print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
# orphan @0x013E
import marshal
import struct
import sys
with open(sys.argv[1], 'rb') as f:
    data = f.read()
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
# orphan @0x0190
raw = data[pos]
'pos '(f"{pos}: consts type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
# orphan @0x01C8
# orphan @0x01D2
# orphan @0x01DA
# orphan @0x01F4
# orphan @0x0202
# orphan @0x0206
# orphan @0x0208
print(f"  {count} constants")
# orphan @0x022A
# orphan @0x022E
raw2 = data[pos]
pos += 1
t2 = raw2 & 127
flags = ''
# orphan @0x0256
ref = struct.unpack('<I', data[pos:pos + 4])[0]
pos += 4
flags = f" (ref={ref})"
# orphan @0x0286
# orphan @0x0290
# orphan @0x02A0
# orphan @0x02A4
# orphan @0x02A6
print(f"  [{i}] child code at offset {child_start}{flags}")
saved = pos
tmp = io.BytesIO(data)
tmp.seek(child_start)
child = marshal.load(tmp)
actual_end = tmp.tell()
print(f"    name={child.co_name} names={child.co_names} varnames={child.co_varnames}")
print(f"    consts={<listcomp>(child.co_consts)}")
pos = actual_end
# orphan @0x032C
# orphan @0x0336
print(f"  [{i}] None{flags}")
# orphan @0x034C
# orphan @0x0356
length = data[pos]
pos += 1
s = data[pos:pos + length].decode('utf-8', errors='replace')
pos += length
print(f"  [{i}] {repr(s)}{flags}")
# orphan @0x03A6
'  ['(f"{i}] type=0x{raw2}{'02X'} (stripped={t2}){flags} -> skip")
tmp = io.BytesIO(data)
tmp.seek(pos - 1)
val = marshal.load(tmp)
pos = tmp.tell()
print(f"    -> {repr(val)}")
# orphan @0x0406
# orphan @0x040A
print(f"pos {pos}: after all constants")
print(f"total file: {len(data)}")
return None
# [SUMMARY] 32 blocks · 7 processed · 25 orphan · 524 instr
