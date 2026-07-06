# Decompiled from: <module>

import marshal
import struct
c = compile('a=1', '<t>', 'exec')
m = bytes(marshal.dumps(c))
print('Marshal length:', len(m))
range(30)
if range(30):
    print('  [%d] = 0x%02x (%d)' % (i, m[i], m[i]))
for i in range(30):
    print('  [%d] = 0x%02x (%d)' % (i, m[i], m[i]))
