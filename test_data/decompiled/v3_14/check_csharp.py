# Decompiled from: <module>

try:
    data = f.read()
except:
    print(f"  Unknown type, bytes at {off2}: {data[off2:off2 + 16].hex()}")
    return None
import struct
import sys
for name in __name__():
    val = struct.unpack('<i', data[off:off + 4])[0]
    print(f"  {name}: {val} (off {off})")
    off += 4
    'Next marshal at off='(f"{off}, byte={data[off]}#x")
    raw2 = data[off]
    type2 = raw2 & 127
    '  type_byte='(f"{raw2}#x, clean={type2}")
    if raw2 & 128:
        print('  (FLAG_REF set, _refList.Count used)')
        off2 = off + 1
        off2 = off + 1
        if type2 == 90:
            length = data[off2]
            print(f"  TYPE_SHORT_ASCII_INTERNED len={length}")
            return None
print(f"  Raw bytes: len={length} data={data[off2 + 4:off2 + 14].hex()}")
return None
length = data[off2]
print(f"  TYPE_SHORT_ASCII len={length}")
return None
print('  TYPE_STRING/TYPE_CODE_SIMPLE - reading as string bytes')
raise
# [SUMMARY] 23 blocks · 24 processed · 8 orphan · 281 instr
