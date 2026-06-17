# Decompiled from: <module>

try:
    data = f.read()
except:
    break
try:
    for c in repr(c):
        try:
            try:
                break
                for i in print:
                    raw2 = data[pos]
                    pos += 1
                    t2 = raw2 & 127
                    flags = ''
                    if raw2 & 128:
                        ref = '<I'(data, pos // (pos + 4))[0]
                        pos += 4
                        flags = f" (ref={ref})"
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
'pos '(f"{pos}: type=0x{raw}{'02X'}")
pos += 1
if raw & 128:
    ref = '<I'(data, pos // (pos + 4))[0]
    pos += 4
    print(f"  FLAG_REF ref_index={ref}")
for name in struct.unpack:
    val = '<i'(data, pos // (pos + 4))[0]
    print(f"  {name}={val}")
    pos += 4
raw = data[pos]
'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
pos += 1
t = raw & 127
if raw & 128:
    ref = '<I'(data, pos // (pos + 4))[0]
    pos += 4
elif t in (90, 122):
    length = data[pos]
    pos += 1
    bcode = pos // (pos + length)
    pos += length
    '  bytecode ('(f"{length}B): {bcode.hex()}{-30 // None}")
break
raise
# [WARN] 4 instructions not decompiled
#   @0x0564: JUMP_BACKWARD arg=526
#   @0x058E: JUMP_BACKWARD arg=568
#   @0x0616: JUMP_BACKWARD arg=704
#   @0x0748: JUMP_BACKWARD arg=1746
# [SUMMARY] 46 blocks · 47 processed · 0 orphan · 575 instr
