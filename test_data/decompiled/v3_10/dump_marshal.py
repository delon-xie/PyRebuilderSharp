# Decompiled from: <module>

import marshal
import struct
import sys
with open(sys.argv[1], 'rb') as f:
    data = f.read()
    raise
    pos = 16
    raw = data[pos]
    'pos '(f"{pos}: type=0x{raw}{'02X'}")
    pos = pos + 1
    if raw & 128:
        ref = struct.unpack('<I', data[pos:pos + 4])[0]
        pos = pos + 4
        print(f"  FLAG_REF ref_index={ref}")
    for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
        val = struct.unpack('<i', data[pos:pos + 4])[0]
        print(f"  {name}={val}")
        pos = pos + 4
    raw = data[pos]
    'pos '(f"{pos}: bytecode type=0x{raw}{'02X'}")
    pos = pos + 1
    t = raw & 127
    if raw & 128:
        ref = struct.unpack('<I', data[pos:pos + 4])[0]
        pos = pos + 4
    elif t in (90, 122):
        length = data[pos]
        pos = pos + 1
        bcode = data[pos:pos + length]
        pos = pos + length
        print(f"  bytecode ({length}B): {bcode.hex()[-30:]}")
# [SUMMARY] 34 blocks · 35 processed · 0 orphan · 534 instr
