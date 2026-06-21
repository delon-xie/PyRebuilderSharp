# Decompiled from: <module>

try:
    data = f.read()
except:
    pass
try:
    []
    for c in []:
        try:
            try:
                []
                break
                for i in range(min(count, 6)):
                    raw2 = data[pos]
                    pos += 1
                    t2 = raw2 & 127
                    flags = ''
                    if raw2 & 128:
                        ref = struct.unpack('<I', data[pos:pos + 4])[0]
                        pos += 4
                        flags = f" (ref={ref})"
                    elif (t2 == 99) and (raw2 & 128):
                        pass
                    else:
                        0
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
__name__()
open(sys.argv[1], 'rb')
__module__
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
raw = data[pos]
'pos '(f"{pos}: bytecode type=0x{raw}02X")
pos += 1
t = raw & 127
if raw & 128:
    ref = struct.unpack('<I', data[pos:pos + 4])[0]
    pos += 4
elif t in (90, 122):
    length = data[pos]
    pos += 1
    bcode = data[pos:pos + length]
    pos += length
    print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
raise
# [WARN] 6 instructions not decompiled
#   @0x01E4: JUMP_BACKWARD arg=360
#   @0x06D4: JUMP_BACKWARD arg=1726
#   @0x06F4: JUMP_BACKWARD arg=1144
#   @0x0724: JUMP_BACKWARD arg=1144
#   @0x07D4: JUMP_BACKWARD arg=1144
#   @0x08BE: JUMP_BACKWARD arg=1144
# [SUMMARY] 45 blocks · 46 processed · 0 orphan · 590 instr
