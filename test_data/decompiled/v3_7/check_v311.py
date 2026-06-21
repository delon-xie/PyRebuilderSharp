# Decompiled from: <module>

with open(sys.argv[1], 'rb') as f:
    raw = f.read()
for off in range(17, 40):
    if raw[off:off + 4] == b'AAAAAA==':
        print(f"  4 zero bytes at offset {off}")
print("""
Bytes 16-50:""")
range(16, 50, 2)
for i in range(16, 50, 2):
    pair = raw[i:i + 2]
    '  '(f"{i}{'3d'}: {pair.hex()}")
# [SUMMARY] 8 blocks · 9 processed · 0 orphan · 238 instr
