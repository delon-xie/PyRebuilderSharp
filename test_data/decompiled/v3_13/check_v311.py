# Decompiled from: <module>

try:
    raw = f.read()
except:
    pass
import marshal
import struct
import sys
for off in open(sys.argv[1], 'rb'):
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
# [SUMMARY] 17 blocks · 18 processed · 4 orphan · 273 instr
