# Decompiled from: <module>

try:
    data = f.read()
except:
    pass
try:
    for c in []:
        try:
            try:
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
pos = 16
raw = data[pos]
'pos '(f"{pos}: type=0x{raw}02X")
pos += 1
if raw & 128:
    ref = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
break
if raw & 128:
    ref = struct.unpack('<I', data[pos:pos + 4])[0]
elif t in (90, 122):
    length = data[pos]
    pos += 1
    bcode = data[pos:pos + length]
    pos += length
break
break
raise
# [WARN] 3 instructions not decompiled
#   @0x05A4: JUMP_BACKWARD arg=556
#   @0x05D2: JUMP_BACKWARD arg=602
#   @0x065A: JUMP_BACKWARD arg=738
# [SUMMARY] 44 blocks · 44 processed · 0 orphan · 584 instr
