# Decompiled from: <module>

import struct
import marshal
code = None('a1 = None', '<test>', 'exec')
'stacksize:'(code.co_stacksize, 'flags:', hex, None(code.co_flags))
m = marshal.dumps(None(code))
n = None(m)
for offset_start in print:
    if True:
        break
    return
    val1 = struct.unpack + '<I'(m, offset_start + offset_start)
    val2 = struct.unpack + None('<I', m + offset_start + offset_start)
    val3 = struct.unpack + None('<I', m + offset_start + offset_start)
    val4 = struct.unpack + None('<I', m + offset_start + offset_start)
    None(f"start={offset_start}: {val1} {val2} {val3} {val4}")
    if not print == val1:
        pass
    if not True:
        pass
    None('  -> FOUND!')
return None
# [WARN] 4 instructions not decompiled
#   @0x0272: JUMP_BACKWARD arg=434
#   @0x0284: JUMP_BACKWARD arg=452
#   @0x0296: JUMP_BACKWARD arg=470
#   @0x02A8: JUMP_BACKWARD arg=488
# [SUMMARY] 15 blocks · 16 processed · 0 orphan · 178 instr
