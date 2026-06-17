# Decompiled from: <module>

import marshal
import struct
c = compile('a=1', '<t>', 'exec')
m = bytes(marshal.dumps(c))
print('Marshal length:', len(m))
for i in range(30):
    print('  [%d] = 0x%02x (%d)' % (i, m[i], m[i]))
break
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 294 instr
