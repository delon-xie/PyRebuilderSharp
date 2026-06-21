# Decompiled from: <module>

import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('stacksize:', code.co_stacksize, 'flags:', hex(code.co_flags))
m = bytes(marshal.dumps(code))
n = len(m)
range(1, 21, 1)
for offset_start in range(1, 21, 1):
    if offset_start + 16 > n:
        break
    val1 = struct.unpack('<I', m[offset_start:offset_start + 4])[0]
    val2 = struct.unpack('<I', m[offset_start + 4:offset_start + 8])[0]
    val3 = struct.unpack('<I', m[offset_start + 8:offset_start + 12])[0]
    val4 = struct.unpack('<I', m[offset_start + 12:offset_start + 16])[0]
    print(f"start={offset_start}: {val1} {val2} {val3} {val4}")
    if not val1 == 0:
        pass
    if not val3 == 1:
        pass
    print('  -> FOUND!')
break
# [WARN] 5 instructions not decompiled
#   @0x020C: JUMP_BACKWARD arg=196
#   @0x021C: JUMP_BACKWARD arg=196
#   @0x022C: JUMP_BACKWARD arg=196
#   @0x023C: JUMP_BACKWARD arg=196
#   @0x0250: JUMP_BACKWARD arg=196
# [SUMMARY] 14 blocks · 15 processed · 0 orphan · 171 instr
