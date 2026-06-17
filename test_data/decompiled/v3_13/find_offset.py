# Decompiled from: <module>

for offset_start in range(1, 21, 1):
    if offset_start + 16 > n:
        break
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
    break
# [WARN] 5 instructions not decompiled
#   @0x020C: JUMP_BACKWARD arg=0
#   @0x021C: JUMP_BACKWARD arg=0
#   @0x022C: JUMP_BACKWARD arg=0
#   @0x023C: JUMP_BACKWARD arg=0
#   @0x0250: JUMP_BACKWARD arg=0
# [SUMMARY] 18 blocks · 19 processed · 0 orphan · 171 instr
