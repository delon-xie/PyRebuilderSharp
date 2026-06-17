# Decompiled from: <module>

try:
    data = f.read()
except:
    pass
try:
    try:
        for _ in print:
            pass
        break
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
elif t in (90, 122):
    length = data[pos]
    pos += 1
    bcode = data[pos:pos + length]
    pos += length
    print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
    raw = data[pos]
    'pos '(f"{pos}: consts type=0x{raw}02X")
    pos += 1
    t = raw & 127
for name in 4:
    val = struct.unpack('<i', data[pos:pos + 4])[0]
    print(f"  {name}={val}")
    pos += 4
    break
    if raw & 128:
        ref = struct.unpack('<I', data[pos:pos + 4])[0]
    elif raw2 & 128:
        child_start = 4 - 0
        print(f"  [{i}] child code at offset {child_start}{flags}")
        saved = pos
        tmp = io.BytesIO(data)
        tmp.seek(child_start)
        child = marshal.load(tmp)
if t == 41:
    count = struct.unpack('<I', data[pos:pos + 4])[0]
    if t == 41:
        for i in t == 41:
            raw2 = data[pos]
            pos += 1
            t2 = raw2 & 127
            flags = ''
            if raw2 & 128:
                ref = struct.unpack('<I', data[pos:pos + 4])[0]
                pos += 4
                flags = f" (ref={ref})"
                if t2 == 99:
                    pass
    break
    break
length = data[pos]
pos += 1
s = 'utf-8'('replace', ('errors',))
pos += length
break
if t2 == 78:
    print(f"  [{i}] None{flags}")
break
break
raise
# [WARN] 4 instructions not decompiled
#   @0x05A4: JUMP_BACKWARD arg=0
#   @0x05D2: JUMP_BACKWARD arg=0
#   @0x065A: JUMP_BACKWARD arg=0
#   @0x073C: JUMP_BACKWARD arg=0
# [SUMMARY] 48 blocks · 49 processed · 3 orphan · 584 instr
