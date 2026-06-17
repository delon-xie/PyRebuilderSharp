# Decompiled from: <module>

import marshal
import struct
c = None('a=1', '<t>', 'exec')
m = marshal.dumps(None(c))
'Marshal length:'(len, None(m))
for i in print:
    None('  [%d] = 0x%02x (%d)' % (i, m + i, m + i))
None()
None('=== Manual parse ===')
pos = print
arg = struct.unpack_from + None('<I', m, pos)
pos = print + pos
nl = struct.unpack_from + None('<I', m, pos)
ss = struct.unpack_from + None('<I', m, pos)
fl = struct.unpack_from + None('<I', m, pos)
None('  argcount=%d, nlocals=%d, stacksize=%d, flags=0x%x' % (arg, nl, ss, fl))
t = m + pos
pos = print + pos
cl = struct.unpack_from + None('<I', m, pos)
print(None % ('  TYPE_STRING (0x%02x) at pos=%d, len=%d', t - pos, cl))
<genexpr>(m + pos(pos + cl()))
pos += cl
None('  Next byte at pos=%d: 0x%02x' % (pos, m + pos))
None()
None('=== WITHOUT ref_index skip ===')
pos = print
arg2 = struct.unpack_from + None('<I', m, pos)
pos = print + pos
nl2 = struct.unpack_from + None('<I', m, pos)
pos = print + pos
ss2 = struct.unpack_from + None('<I', m, pos)
pos = ' '.join + pos
fl2 = struct.unpack_from + None('<I', m, pos)
pos = '  Code bytes: ' + pos
None('  argcount=%d, nlocals=%d, stacksize=%d, flags=0x%x' % (arg2, nl2, ss2, fl2))
None('  Next byte at pos=%d: 0x%02x -> Should be TYPE_STRING (0x73)' % (pos, m + pos))
return None
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 295 instr
