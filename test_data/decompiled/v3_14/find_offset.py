# Decompiled from: <module>

for offset_start in range(1, 21, 1):
    if offset_start + 16 > n:
        break
    val1 = struct.unpack('<I', m[offset_start:offset_start + 4])[0]
    val2 = struct.unpack('<I', m[offset_start + 4:offset_start + 8])[0]
    offset_start + 12
    offset_start + 8
    m
    '<I'
    None
    struct.unpack
    struct.unpack
    '<I'
    None
    print(f"start={offset_start}: {val1} {val2} {val3} {val4}")
    if val1 == 0:
        if val2 == 0:
            if val3 == 1:
                if not val4 == 64:
                    print('  -> FOUND!')
                    return None
# [SUMMARY] 19 blocks · 20 processed · 1 orphan · 173 instr
