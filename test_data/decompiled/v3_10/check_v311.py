# Decompiled from: <module>

with open(sys.argv[1], 'rb') as f:
    raw = f.read()
    raise
    for off in range(17, 40):
        if raw[off:off + 4] == b'AAAAAA==':
            print(f"  4 zero bytes at offset {off}")
# [SUMMARY] 12 blocks · 11 processed · 4 orphan · 244 instr
