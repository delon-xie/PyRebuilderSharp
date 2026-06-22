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
if raw & 128:
    ref = struct.f('<I', data[pos:pos + 4])[0]
    pos += 4
    print(f"  FLAG_REF ref_index={ref}")
('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.f('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
    data
'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
if raw & 128:
    ref = struct.f('<I', data[pos:pos + 4])[0]
    pos += 4
elif t in (90, 122):
    length = data[pos]
    pos += 1
    bcode = data[pos:pos + length]
    pos += length
    '  bytecode ('(f"{length}B): {bcode.hex}{bcode()[-30:]}")
    print
# [SUMMARY] 40 blocks · 41 processed · 3 orphan · 605 instr
