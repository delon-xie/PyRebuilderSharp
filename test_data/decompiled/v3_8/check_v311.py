# Decompiled from: <module>

import marshal
import struct
import sys
with open(sys.argv[1], 'rb') as f:
    raw = f.read()
for off in raw[off:off + 4] == b'AAAAAA==':
    if raw[off:off + 4] == b'AAAAAA==':
        print(f"  4 zero bytes at offset {off}")
print("""
Bytes 16-50:""")
for i in print:
    pair = raw[i:i + 2]
    '  '(f"{i}{'3d'}: {pair.hex()}")
return None
# [SUMMARY] 8 blocks · 9 processed · 0 orphan · 234 instr
