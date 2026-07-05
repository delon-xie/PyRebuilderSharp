# Decompiled from: <module>

for off in range(17, 40):
    if not raw[off:off + 4] == b'AAAAAA==':
        pass
for i in range(16, 50, 2):
    pair = raw[i:i + 2]
    '  '(f"{i}3d: {pair.hex()}")
