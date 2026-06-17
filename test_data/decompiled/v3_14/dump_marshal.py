# Decompiled from: <module>

try:
    data = f.read()
except:
    pass
try:
    for c in []:
        try:
            try:
                break
                for i in print:
                    raw2 = data[pos]
                    pos += 1
                    t2 = raw2 & 127
                    flags = ''
                    if raw2 & 128:
                        ref = struct.unpack('<I', data[pos:pos + 4])[0]
                        pos += 4
                    elif (t2 == 99) and (raw2 & 128):
                        pass
                print(f"pos {pos}: after all constants")
                print(f"total file: {len(data)}")
                return None
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
raw = data[pos]
'pos '(f"{pos}: bytecode type=0x{raw}02X")
pos += 1
t = raw & 127
if raw & 128:
    ref = struct.unpack('<I', data[pos:pos + 4])[0]
elif t in (90, 122):
    length = data[pos]
    pos += 1
    bcode = data[pos:pos + length]
    pos += length
raise
# [WARN] 3 instructions not decompiled
#   @0x06F4: JUMP_BACKWARD arg=640
#   @0x0724: JUMP_BACKWARD arg=688
#   @0x07D4: JUMP_BACKWARD arg=864
# [SUMMARY] 45 blocks · 46 processed · 0 orphan · 602 instr
