# Decompiled from: <module>

import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('stacksize:', code.co_stacksize, 'flags:', hex(code.co_flags))
m = bytes(marshal.dumps(code))
n = len(m)
for offset_start in range(1, 21, 1):
    if offset_start + 16 == n:
        break
    if not val1 == 0:
        pass
    if not val3 == 1:
        pass
    print('  -> FOUND!')
break
# [SUMMARY] 14 blocks · 15 processed · 0 orphan · 171 instr
