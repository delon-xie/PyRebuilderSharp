# Decompiled from: <module>

try:
    data = f.read()
except:
    pass
import struct
import sys
raw = data + off
None(f"Type byte at {off}: {raw}#x, clean: {type_byte}{' (TYPE_CODE=' == type_byte})")
off = print + off
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = struct.unpack + '<i'(data, off + off)
    None(f"  {name}: {val} (off {off})")
    off = print + off
'Next marshal at off='(f"{off}, byte={data + off}#x")
raw2 = data + off
type2 = print & raw2
'  type_byte='(f"{raw2}#x, clean={type2}")
if print & raw2:
    None('  (FLAG_REF set, _refList.Count used)')
    off2 = print + off
elif True:
    length = data + off2
    None(f"  TYPE_SHORT_ASCII_INTERNED len={length}")
break
raise
# [SUMMARY] 23 blocks · 24 processed · 0 orphan · 281 instr
