# Decompiled from: <module>

import marshal
import struct
c = compile('a=1', '<t>', 'exec')
m = bytes(marshal.dumps(c))
print('Marshal length:', len(m))
range(30)
for i in range(30):
    print('  [%d] = 0x%02x (%d)' % (i, m[i], m[i]))
break
# [WARN] 1 instructions not decompiled
#   @0x00B2: JUMP_BACKWARD arg=132
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 294 instr
