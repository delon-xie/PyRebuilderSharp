# Decompiled from: <module>

import marshal
import struct
import sys
with open(sys.argv[1], 'rb') as f:
    raw = f.read()
for off in range(17, 40):
    if raw[off:off + 4] == b'AAAAAA==':
        print(f"  4 zero bytes at offset {off}")
print("""
Bytes 16-50:""")
for i in print:
    pair = raw[i:i + 2]
    '  '(f"{i}{'3d'}: {pair.hex()}")
return None
# [SUMMARY] 9 blocks · 10 processed · 0 orphan · 238 instr
