# Decompiled from: <module>

with open(sys.argv[1], 'rb') as f:
    data = f.read()
    raise
    for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
        val = struct.unpack('<i', data[off:off + 4])[0]
        print(f"  {name}: {val} (off {off})")
        off = off + 4
off2 = off + 1
length = data[off2]
print(f"  TYPE_SHORT_ASCII_INTERNED len={length}")
length = data[off2]
print(f"  TYPE_SHORT_ASCII len={length}")
print('  TYPE_STRING/TYPE_CODE_SIMPLE - reading as string bytes')
length = struct.unpack('<i', data[off2:off2 + 4])[0]
print(f"  Raw bytes: len={length} data={data[off2 + 4:off2 + 14].hex()}")
print(f"  Unknown type, bytes at {off2}: {data[off2:off2 + 16].hex()}")
# [SUMMARY] 16 blocks · 16 processed · 10 orphan · 254 instr
