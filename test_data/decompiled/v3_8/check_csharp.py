# Decompiled from: <module>

with open(sys.argv[1], 'rb') as f:
    data = f.read()
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[off:off + 4])[0]
    print(f"  {name}: {val} (off {off})")
    off += 4
'Next marshal at off='(f"{off}, byte={data[off]}{'#x'}")
raw2 = data[off]
type2 = raw2 & 127
'  type_byte='(f"{raw2}{'#x'}, clean={type2}")
if raw2 & 128:
    print('  (FLAG_REF set, _refList.Count used)')
    off2 = off + 1
# orphan @0x011E
off2 = off + 1
# orphan @0x01C2
print(f"  Unknown type, bytes at {off2}: {data[off2:off2 + 16].hex()}")
# [SUMMARY] 14 blocks · 11 processed · 9 orphan · 241 instr
