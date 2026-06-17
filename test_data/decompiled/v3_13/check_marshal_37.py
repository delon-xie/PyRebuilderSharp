# Decompiled from: <module>

for offset in range(0, 8):
    if vals[0] == code.co_argcount:
        pass
    if not vals[3] == code.co_flags:
        pass
    print(f"
Fields found at offset {offset}:")
    print(f"  [arg={vals[0]}, nlocals={vals[1]}, stacksize={vals[2]}, flags={hex(vals[3])}]")
    '  Bytes: '(f"{' '.join}{<genexpr>(m[offset:offset + 16]())}")
    break
# [WARN] 3 instructions not decompiled
#   @0x0202: JUMP_BACKWARD arg=0
#   @0x022C: JUMP_BACKWARD arg=0
#   @0x02E4: JUMP_BACKWARD arg=0
# [SUMMARY] 13 blocks · 14 processed · 1 orphan · 196 instr
