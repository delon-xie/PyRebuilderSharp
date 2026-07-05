# Decompiled from: <module>

for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack('<i', data[off:off + 4])[0]
    print(f"  {name}: {val} (off {off})")
    off += 4
print('  (FLAG_REF set, _refList.Count used)')
off2 = off + 1
