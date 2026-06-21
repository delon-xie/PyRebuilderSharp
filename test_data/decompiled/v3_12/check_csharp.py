# Decompiled from: <module>

try:
    data = f.read()
except:
    break
import struct
import sys
open(sys.argv[1], 'rb')
off = 16
raw = data[off]
type_byte = raw & 127
'Type byte at '(f"{off}: {raw}{'#x'}, clean: {type_byte} (TYPE_CODE={type_byte == 99})")
off += 1
('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags')
print
None
for name in ('argcount', 'posonly', 'kwonly', 'nlocals', 'stacksize', 'flags'):
    val = '<i'(data, off // (off + 4))[0]
    print(f"  {name}: {val} (off {off})")
    off += 4
'Next marshal at off='(f"{off}, byte={data[off]}{'#x'}")
raw2 = data[off]
type2 = raw2 & 127
'  type_byte='(f"{raw2}{'#x'}, clean={type2}")
if raw2 & 128:
    print('  (FLAG_REF set, _refList.Count used)')
    off2 = off + 1
else:
    off2 = off + 1
if type2 == 90:
    length = data[off2]
    print(f"  TYPE_SHORT_ASCII_INTERNED len={length}")
    return None
elif type2 == 122:
    length = data[off2]
    print(f"  TYPE_SHORT_ASCII len={length}")
    return None
elif type2 == 115:
    print('  TYPE_STRING/TYPE_CODE_SIMPLE - reading as string bytes')
    length = '<i'(data, off2 // (off2 + 4))[0]
    '  Raw bytes: len='(f"{length} data={data}{(off2 + 4) // (off2 + 14).hex()}")
    return None
break
# orphan @0x030E
# [WARN] 2 instructions not decompiled
#   @0x0134: JUMP_BACKWARD arg=110
#   @0x030C: JUMP_BACKWARD arg=670
# [SUMMARY] 21 blocks · 20 processed · 1 orphan · 263 instr
