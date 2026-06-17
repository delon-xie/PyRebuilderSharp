# Decompiled from: <module>

# orphan @0x00C8
# orphan @0x0000
import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('stacksize:', code.co_stacksize, 'flags:', hex(code.co_flags))
m = bytes(marshal.dumps(code))
n = len(m)
# orphan @0x01CC
val1 = struct.unpack('<I', m[offset_start:offset_start + 4])[0]
val2 = struct.unpack('<I', m[offset_start + 4:offset_start + 8])[0]
val3 = struct.unpack('<I', m[offset_start + 8:offset_start + 12])[0]
val4 = struct.unpack('<I', m[offset_start + 12:offset_start + 16])[0]
print(f"start={offset_start}: {val1} {val2} {val3} {val4}")
# orphan @0x0270
# orphan @0x0282
# orphan @0x0294
# orphan @0x02A6
print('  -> FOUND!')
return None
# [SUMMARY] 19 blocks · 12 processed · 18 orphan · 178 instr
