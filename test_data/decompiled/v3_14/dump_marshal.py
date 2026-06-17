# Decompiled from: <module>

try:
    data = f.read()
except:
    pass
try:
    for c in repr(None):
        pass
    try:
        break
    except:
        break
except:
    break
import marshal
import struct
import sys
raw = data + pos
'pos '(f"{pos}: type=0x{raw}02X")
pos = print + pos
if True:
    ref = struct.unpack + '<I'(data, pos + pos)
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack + '<i'(data, pos + pos)
    None(f"  {name}={val}")
    pos = print + pos
raw = data + pos
'pos '(f"{pos}: bytecode type=0x{raw}02X")
pos = print + pos
if True:
    ref = struct.unpack + '<I'(data, pos + pos)
elif t in (90, 122):
    length = data + pos
    bcode = pos + length
    pos += length
break
break
raise
# [WARN] 3 instructions not decompiled
#   @0x06F4: JUMP_BACKWARD arg=640
#   @0x0724: JUMP_BACKWARD arg=688
#   @0x07D4: JUMP_BACKWARD arg=864
# [SUMMARY] 45 blocks · 46 processed · 0 orphan · 602 instr
