# Decompiled from: <module>

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
    if not val2 == 0:
        pass
    if not val3 == 1:
        pass
    if not val4 == 64:
        pass
    print('  -> FOUND!')
    return None
# [WARN] 5 instructions not decompiled
#   @0x0272: JUMP_BACKWARD arg=0
#   @0x0284: JUMP_BACKWARD arg=0
#   @0x0296: JUMP_BACKWARD arg=0
#   @0x02A8: JUMP_BACKWARD arg=0
#   @0x02BC: JUMP_BACKWARD arg=0
# [SUMMARY] 19 blocks · 20 processed · 1 orphan · 178 instr
