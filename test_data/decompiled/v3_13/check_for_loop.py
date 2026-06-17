# Decompiled from: <module>

for instr in dis.get_instructions(code):
    instr.offset(f"3d opname={instr.opname}25s arg={instr.arg} argrepr={instr.argrepr}")
    break
# [WARN] 1 instructions not decompiled
#   @0x0174: JUMP_BACKWARD arg=0
# [SUMMARY] 4 blocks · 5 processed · 0 orphan · 93 instr
