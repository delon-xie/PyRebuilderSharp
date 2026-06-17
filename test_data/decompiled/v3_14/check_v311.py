# Decompiled from: <module>

try:
    raw = f.read()
except:
    pass
import marshal
import struct
import sys
for off in __name__():
    if raw[off:off + 4] == b'AAAAAA==':
        pass
    else:
        print(f"  4 zero bytes at offset {off}")
        print("""
Bytes 16-50:""")
    pair = raw[i:i + 2]
    '  '(f"{i}3d: {pair.hex()}")
    return None
raise
# [SUMMARY] 17 blocks · 18 processed · 4 orphan · 280 instr
