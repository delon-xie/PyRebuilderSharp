# Decompiled from: <module>

with open(sys.argv[1], 'rb') as f:
    data = f.read()
    for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
        val = struct.unpack('<i', data[off:off + 4])[0]
        print(f"  {name}: {val} (off {off})")
        off = off + 4
# orphan @0x0132
off2 = off + 1
# orphan @0x01D6
print(f"  Unknown type, bytes at {off2}: {data[off2:off2 + 16].hex()}")
# [SUMMARY] 17 blocks · 14 processed · 11 orphan · 251 instr
