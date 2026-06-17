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
    for name in raw & 128:
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
            if t in (90, 122):
                pass
            break
        child_start = 4 - 0
        print(f"  [{i}] child code at offset {child_start}{flags}")
        saved = pos
        tmp = io.BytesIO(data)
        tmp.seek(child_start)
        child = marshal.load(tmp)
        actual_end = tmp.tell()
length = data[pos]
pos += 1
bcode = data[pos:pos + length]
pos += length
print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
raw = data[pos]
'pos '(f"{pos}: consts type=0x{raw}02X")
pos += 1
t = raw & 127
if (t in (40, 41)) and (t == 41):
    pass
break
break
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
if t2 == 78:
    print(f"  [{i}] None{flags}")
    if t2 in (122, 90):
        length = data[pos]
        pos += 1
        s = 'utf-8'('replace', ('errors',))
        pos += length
pos = tmp.tell()
print(f"    -> {repr(val)}")
print(f"pos {pos}: after all constants")
print(f"total file: {len(data)}")
return None
raise
# [SUMMARY] 48 blocks · 49 processed · 9 orphan · 602 instr
