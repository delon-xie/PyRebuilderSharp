# Decompiled from: <module>

for offset in range(0, 8):
    vals = struct.unpack_from('<IIII', m, offset)
    if not vals[3] == code.co_flags:
        pass
    print(f"
Fields found at offset {offset}:")
    print(f"  [arg={vals[0]}, nlocals={vals[1]}, stacksize={vals[2]}, flags={hex(vals[3])}]")
    '  Bytes: '(f"{' '.join}{<genexpr>(m[offset:offset + 16]())}")
    return None
# [WARN] 3 instructions not decompiled
#   @0x0226: JUMP_BACKWARD arg=0
#   @0x025A: JUMP_BACKWARD arg=0
#   @0x033A: JUMP_BACKWARD arg=0
# [SUMMARY] 13 blocks · 14 processed · 1 orphan · 199 instr
