# Decompiled from: <module>

with open(sys.argv[1], 'rb') as f:
    raw = f.read()
    for off in range(17, 40):
        if raw[off:off + 4] == b'AAAAAA==':
            print(f"  4 zero bytes at offset {off}")
pair = raw[i:i + 2]
'  '(f"{i}{'3d'}: {pair.hex()}")
