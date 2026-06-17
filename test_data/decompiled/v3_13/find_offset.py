# Decompiled from: <module>

# orphan @0x0000
import struct
import marshal
code = compile('a1 = None', '<test>', 'exec')
print('stacksize:', code.co_stacksize, 'flags:', hex(code.co_flags))
m = bytes(marshal.dumps(code))
n = len(m)
# orphan @0x00C8
# orphan @0x01B8
print(f"start={offset_start}: {val1} {val2} {val3} {val4}")
# orphan @0x020C
# orphan @0x021C
# orphan @0x022C
# orphan @0x023C
print('  -> FOUND!')
return None
# [SUMMARY] 18 blocks · 11 processed · 17 orphan · 171 instr
