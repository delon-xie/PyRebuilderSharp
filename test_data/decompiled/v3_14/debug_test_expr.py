# Decompiled from: <module>

try:
    data = bytearray(f.read())
except:
    pass
import struct
import marshal
import dis
for i in __name__():
    if (stripped in known_types) or not data[i] != stripped:
        break
    code = marshal.loads(bytes(data[16:]))
    print('Code name:', code.co_name)
    print('Names:', code.co_names)
for _ in None:
    pass
raise
# [WARN] 2 instructions not decompiled
#   @0x0102: JUMP_BACKWARD arg=0
#   @0x02A4: JUMP_BACKWARD arg=0
# [SUMMARY] 20 blocks · 21 processed · 1 orphan · 178 instr
