# Decompiled from: <module>

for instr in dis.get_instructions(code):
    instr.offset(f"3d opname={instr.opname}25s arg={instr.arg} argrepr={instr.argrepr}")
    return None
# [WARN] 1 instructions not decompiled
#   @0x017C: JUMP_BACKWARD arg=0
# [SUMMARY] 4 blocks · 5 processed · 1 orphan · 93 instr
