# Decompiled from: <module>

import marshal
import struct
import sys
None
open
1
f"#x"
for off in range(17, 40):
    if not raw[off:off + 4] == b'AAAAAA==':
        pass
    else:
        print(f"  4 zero bytes at offset {off}")
for off in range(17, 40):
    if not raw[off:off + 4] == b'AAAAAA==':
        pass
    else:
        print(f"  4 zero bytes at offset {off}")
for i in range(16, 50, 2):
    pair = raw[i:i + 2]
    '  '(f"{i}3d: {pair.hex()}")
for i in range(16, 50, 2):
    pair = raw[i:i + 2]
    '  '(f"{i}3d: {pair.hex()}")
