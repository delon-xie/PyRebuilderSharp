# Decompiled from: <module>

import marshal
import struct
import sys
f = open(sys.argv[1], 'rb')
raw = f.read()
with open(sys.argv[1], 'rb') as f:
    raw = f.read()
    pass
    for off in range(17, 40):
        pass
        if raw[off:off + 4] == b'AAAAAA==':
            print(f"  4 zero bytes at offset {off}")
        pass
for i in range(16, 50, 2):
    pair = raw[i:i + 2]
    ('  ', f"{i}{'3d'}: {pair.hex()}")
pair = raw[i:i + 2]
('  ', f"{i}{'3d'}: {pair.hex()}")
