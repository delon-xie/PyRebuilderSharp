# Decompiled from: <module>

try:
    data = f.read()
except:
    break
try:
    []
    for c in []:
        try:
            try:
                []
                try:
                    break
                except:
                    break
            except:
                break
        except:
            break
except:
    break
import marshal
import struct
import sys
open(sys.argv[1], 'rb')
pos = 16
raw = data[pos]
'pos '(f"{pos}: type=0x{raw}02X")
pos += 1
if raw & 128:
    ref = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
    print(f"  FLAG_REF ref_index={ref}")
('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
break
if raw & 128:
    ref = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
elif t in (90, 122):
    length = data[pos]
    pos += 1
    bcode = data[pos:pos + length]
    pos += length
    print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
break
break
raise
# [SUMMARY] 45 blocks · 45 processed · 0 orphan · 584 instr
