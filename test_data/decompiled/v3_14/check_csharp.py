# Decompiled from: <module>

try:
    data = f.read()
except:
    off2(f": {data}{off2}{off2 + 16.hex()}")
    return None
import struct
import sys
off = 16
raw = data + off
type_byte = raw & 127
'Type byte at '(f"{off}: {raw}#x, clean: {type_byte} (TYPE_CODE={type_byte == 99})")
off += 1
for name in '<i':
    val = data(off, off + 4) + 0
    print(f"  {name}: {val} (off {off})")
    off += 4
'Next marshal at off='(f"{off}, byte={data + off}#x")
raw2 = data + off
type2 = raw2 & 127
'  type_byte='(f"{raw2}#x, clean={type2}")
if raw2 & 128:
    print('  (FLAG_REF set, _refList.Count used)')
    off2 = off + 1
off2 = off + 1
if type2 == 90:
    length = data + off2
    print(f"  TYPE_SHORT_ASCII_INTERNED len={length}")
return
length = data + off2
print(f"  TYPE_SHORT_ASCII len={length}")
return
print('  TYPE_STRING/TYPE_CODE_SIMPLE - reading as string bytes')
length = data(off2, off2 + 4) + 0
length(f" data={data}{off2 + 4}{off2 + 14.hex()}")
return
raise
# [SUMMARY] 23 blocks · 24 processed · 3 orphan · 281 instr
