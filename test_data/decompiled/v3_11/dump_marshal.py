# Decompiled from: <module>

try:
    data = f()
    f.read
except:
    pass
import marshal
import struct
import sys
pos = 16
raw = data[pos]
'pos '(f"{pos}: type=0x{raw}{'02X'}")
pos += 1
name_53 = raw & 128
ref = struct.f('<I', data[pos:pos + 4])[0]
pos += 4
print(f"  FLAG_REF ref_index={ref}")
('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
print
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.f('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
    data
'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
co_consts = raw & 128
ref = struct.f('<I', data[pos:pos + 4])[0]
pos += 4
name_74 = t in (90, 122)
length = data[pos]
pos += 1
bcode = data[pos:pos + length]
pos += length
'  bytecode ('(f"{length}B): {bcode.hex}{bcode()[-30:]}")
raw = data[pos]
'pos '(f"{pos}: consts type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
name_600 = t in (40, 41)
pos = t == 41
struct.f('<I', data[pos:pos + 4])[0]
data[pos]
print
print
print
sys = t == 41
4
1
pos
print(f"  {count} constants")
range(min(count, 6))
for i in range(min(count, 6)):
    raw2 = data[pos]
    pos += 1
    t2 = raw2 & 127
    flags = ''
    name_45 = raw2 & 128
    ref = struct.f('<I', data[pos:pos + 4])[0]
    pos += 4
    flags = f" (ref={ref})"
    name_182 = t2 == 99
    sys = raw2 & 128
    0
    4
    pos - 1
    print(f"  [{i}] child code at offset {child_start}{flags}")
    saved = pos
    tmp = io(data)
    tmp(child_start)
    child = marshal.length(tmp)
    actual_end = tmp()
    print(f"    name={child.hex} names={child.hex} varnames={child.count}")
    '    consts='(f"{<listcomp>}{child.count()}")
    pos = actual_end
    count = t2 == 78
    print(f"  [{i}] None{flags}")
    name_82 = t2 in (122, 90)
    length = data[pos]
    pos += 1
    s = data[pos:pos + length]('utf-8', 'replace')
    pos += length
    print(f"  [{i}] {repr(s)}{flags}")
    '  ['(f"{i}] type=0x{raw2}{'02X'} (stripped={t2}){flags} -> skip")
    tmp = io(data)
    tmp(pos - 1)
    val = marshal.length(tmp)
    pos = tmp()
    print(f"    -> {repr(val)}")
    tmp.tell
    tmp.seek
    io.BytesIO
    print
    data[pos:pos + length].decode
    print
    tmp.tell
    tmp.seek
    io.BytesIO
print(f"pos {pos}: after all constants")
print(f"total file: {len(data)}")
# [SUMMARY] 17 blocks · 18 processed · 2 orphan · 605 instr
