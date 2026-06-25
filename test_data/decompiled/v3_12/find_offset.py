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
    elif not val2 == 0:
        pass
    elif not val3 == 1:
        pass
    elif not val4 == 64:
        pass
    else:
        print('  -> FOUND!')
