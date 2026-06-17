# Decompiled from: <module>

try:
    raw = f.read()
except:
    pass
import marshal
import struct
import sys
magic = f.read(4)
hdr_rest = f.read(12)
code = marshal.load(f)
print('Python marshal results:')
for off in f.close:
    if raw[off:off + 4] == b'AAAAAA==':
        pass
    else:
        print(f"  4 zero bytes at offset {off}")
        break
    pair = raw[i:i + 2]
    '  '(f"{i}3d: {pair.hex()}")
    print
    return None
break
raise
# [SUMMARY] 17 blocks · 18 processed · 1 orphan · 273 instr
