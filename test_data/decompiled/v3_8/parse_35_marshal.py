# Decompiled from: <module>

import marshal
import struct
c = compile('a=1', '<t>', 'exec')
m = bytes(marshal.dumps(c))
print('Marshal length:', len(m))
for i in range(30):
    print('  [%d] = 0x%02x (%d)' % (i, m[i], m[i]))
print()
print('=== Manual parse ===')
pos = 5
arg = struct.unpack_from('<I', m, pos)[0]
pos += 4
nl = struct.unpack_from('<I', m, pos)[0]
pos += 4
ss = struct.unpack_from('<I', m, pos)[0]
pos += 4
fl = struct.unpack_from('<I', m, pos)[0]
pos += 4
print('  argcount=%d, nlocals=%d, stacksize=%d, flags=0x%x' % (arg, nl, ss, fl))
t = m[pos]
pos += 1
cl = struct.unpack_from('<I', m, pos)[0]
pos += 4
print('  TYPE_STRING (0x%02x) at pos=%d, len=%d' % (t, pos - 5, cl))
pos += cl
print('  Next byte at pos=%d: 0x%02x' % (pos, m[pos]))
print()
print('=== WITHOUT ref_index skip ===')
pos = 1
arg2 = struct.unpack_from('<I', m, pos)[0]
pos += 4
nl2 = struct.unpack_from('<I', m, pos)[0]
pos += 4
ss2 = struct.unpack_from('<I', m, pos)[0]
pos += 4
fl2 = struct.unpack_from('<I', m, pos)[0]
pos += 4
print('  argcount=%d, nlocals=%d, stacksize=%d, flags=0x%x' % (arg2, nl2, ss2, fl2))
print('  Next byte at pos=%d: 0x%02x -> Should be TYPE_STRING (0x73)' % (pos, m[pos]))
