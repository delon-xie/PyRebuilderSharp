# Decompiled from: <module>

try:
    data = f.read()
except:
    pass
import struct
import sys
for name in open(sys.argv[1], 'rb'):
    val = struct.unpack('<i', data[off:off + 4])[0]
    print(f"  {name}: {val} (off {off})")
    off += 4
    break
    if raw2 & 128:
        print('  (FLAG_REF set, _refList.Count used)')
        off2 = off + 1
        off2 = off + 1
        if type2 == 90:
            length = data[off2]
            print(f"  TYPE_SHORT_ASCII_INTERNED len={length}")
            return None
            if type2 == 122:
                length = data[off2]
                print(f"  TYPE_SHORT_ASCII len={length}")
                return None
print('  TYPE_STRING/TYPE_CODE_SIMPLE - reading as string bytes')
length = struct.unpack('<i', data[off2:off2 + 4])[0]
print(f"  Raw bytes: len={length} data={data[off2 + 4:off2 + 14].hex()}")
return None
break
raise
# [SUMMARY] 20 blocks · 21 processed · 3 orphan · 266 instr
