# Decompiled from: <module>

# orphan @0x0081
arg = struct.unpack_from('<I', m, pos)[0]
pos += 4
nl = struct.unpack_from('<I', m, pos)[0]
pos += 4
ss = struct.unpack_from('<I', m, pos)[0]
pos += 4
fl = struct.unpack_from('<I', m, pos)[0]
pos += 4
pos += 1
cl = struct.unpack_from('<I', m, pos)[0]
pos += 4
pos = cl
arg2 = struct.unpack_from('<I', m, pos)[0]
pos += 4
nl2 = struct.unpack_from('<I', m, pos)[0]
pos += 4
ss2 = struct.unpack_from('<I', m, pos)[0]
pos += 4
fl2 = struct.unpack_from('<I', m, pos)[0]
pos += 4
return
for i in range(30):
    for _ in range(30):
        pass
# orphan @0x5780
# [SUMMARY] 5 blocks · 4 processed · 2 orphan · 257 instr
