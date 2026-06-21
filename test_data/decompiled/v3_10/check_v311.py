# Decompiled from: <module>

with open(sys.argv[1], 'rb') as f:
    raw = f.read()
    raise
    for off in range(17, 40):
        if raw[off:off + 4] == b'AAAAAA==':
            print(f"  4 zero bytes at offset {off}")
# orphan @0x01A0
print("""
Bytes 16-50:""")
range(16, 50, 2)
# orphan @0x01B4
# orphan @0x01B6
pair = raw[i:i + 2]
'  '(f"{i}{'3d'}: {pair.hex()}")
print
# [SUMMARY] 12 blocks · 8 processed · 4 orphan · 244 instr
