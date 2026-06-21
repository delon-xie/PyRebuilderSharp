# Decompiled from: <module>

try:
    raw = f.read()
except:
    pass
import marshal
import struct
import sys
sys.argv
None
open
'rb'
__name__()
__module__
for off in range(17, 40):
    if raw[off:off + 4] == b'AAAAAA==':
        for i in range(16, 50, 2):
            pair = raw[i:i + 2]
            '  '(f"{i}3d: {pair.hex()}")
            return None
raise
# [SUMMARY] 17 blocks · 18 processed · 1 orphan · 278 instr
