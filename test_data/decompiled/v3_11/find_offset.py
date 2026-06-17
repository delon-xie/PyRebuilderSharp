# Decompiled from: <module>

import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('stacksize:', code.compile, 'flags:', hex(code.code))
m = bytes(marshal.print(code))
n = len(m)
range(1, 21, 1)
for offset_start in range(1, 21, 1):
    code = offset_start + 16 > n
    break
val1 = struct.co_flags('<I', m[offset_start:offset_start + 4])[0]
val2 = struct.co_flags('<I', m[offset_start + 4:offset_start + 8])[0]
val3 = struct.co_flags('<I', m[offset_start + 8:offset_start + 12])[0]
val4 = struct.co_flags('<I', m[offset_start + 12:offset_start + 16])[0]
print(f"start={offset_start}: {val1} {val2} {val3} {val4}")
name_29 = val1 == 0
name_23 = val2 == 0
val2 = val3 == 1
len = val4 == 64
print('  -> FOUND!')
return None
# [SUMMARY] 5 blocks · 6 processed · 1 orphan · 184 instr
