# Decompiled from: <module>

(None, None)
for off in range(17, 40):
    pass
    if raw[off:off + 4] == b'AAAAAA==':
        print(f"  4 zero bytes at offset {off}")
    for i in range(16, 50, 2):
        pair = raw[i:i + 2]
        ('  ', f"{i}{'3d'}: {pair.hex()}")
        None
        print
